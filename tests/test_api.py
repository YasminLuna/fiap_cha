from fastapi.testclient import TestClient

from tests.factories import order_payload


def open_order(client: TestClient, auth: dict[str, str], catalog: dict, *, parts=None):
    payload = order_payload(
        catalog["client"]["id"],
        catalog["vehicle"]["id"],
        [catalog["service"]["id"]],
        parts=parts or {},
    )
    response = client.post("/api/v1/orders", headers=auth, json=payload)
    assert response.status_code == 201
    return response.json()


def move_to_awaiting_approval(client: TestClient, auth: dict[str, str], order_id: str):
    for status in ("DIAGNOSIS", "AWAITING_APPROVAL"):
        response = client.patch(
            f"/api/v1/orders/{order_id}/status",
            headers=auth,
            json={"status": status},
        )
        assert response.status_code == 200


def test_critical_order_flow_updates_stock_and_notifies(client, auth, catalog, notification_mock):
    order = open_order(
        client,
        auth,
        catalog,
        parts={catalog["part"]["id"]: 1},
    )
    assert order["total"] == "225.00"

    move_to_awaiting_approval(client, auth, order["id"])
    approved = client.post(
        f"/api/v1/orders/{order['id']}/budget-decision",
        json={"decision": "APPROVED", "external_reference": "webhook-001"},
    )

    assert approved.status_code == 200
    assert approved.json()["status"] == "IN_PROGRESS"
    assert notification_mock.call_count == 3
    notification_mock.assert_called_with(catalog["client"]["email"], order["id"], "IN_PROGRESS")

    parts = client.get("/api/v1/parts", headers=auth).json()
    assert parts[0]["stock"] == 9


def test_budget_can_be_rejected(client, auth, catalog, notification_mock):
    order = open_order(client, auth, catalog)
    move_to_awaiting_approval(client, auth, order["id"])

    response = client.post(
        f"/api/v1/orders/{order['id']}/budget-decision",
        json={"decision": "REJECTED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"
    notification_mock.assert_called_with(catalog["client"]["email"], order["id"], "CANCELLED")


def test_active_list_orders_by_priority_and_creation(client, auth, catalog):
    received = open_order(client, auth, catalog)
    diagnosis = open_order(client, auth, catalog)
    awaiting = open_order(client, auth, catalog)
    in_progress = open_order(client, auth, catalog)

    client.patch(
        f"/api/v1/orders/{diagnosis['id']}/status",
        headers=auth,
        json={"status": "DIAGNOSIS"},
    )
    move_to_awaiting_approval(client, auth, awaiting["id"])
    move_to_awaiting_approval(client, auth, in_progress["id"])
    client.post(
        f"/api/v1/orders/{in_progress['id']}/budget-decision",
        json={"decision": "APPROVED"},
    )

    listed = client.get("/api/v1/orders", headers=auth)

    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [
        in_progress["id"],
        awaiting["id"],
        diagnosis["id"],
        received["id"],
    ]


def test_finished_and_delivered_orders_are_removed_from_active_list(client, auth, catalog):
    order = open_order(client, auth, catalog)
    move_to_awaiting_approval(client, auth, order["id"])
    client.post(
        f"/api/v1/orders/{order['id']}/budget-decision",
        json={"decision": "APPROVED"},
    )
    client.patch(
        f"/api/v1/orders/{order['id']}/status",
        headers=auth,
        json={"status": "FINISHED"},
    )

    assert client.get("/api/v1/orders", headers=auth).json() == []


def test_open_order_rejects_insufficient_stock(client, auth, catalog):
    response = client.post(
        "/api/v1/orders",
        headers=auth,
        json=order_payload(
            catalog["client"]["id"],
            catalog["vehicle"]["id"],
            [catalog["service"]["id"]],
            parts={catalog["part"]["id"]: 999},
        ),
    )

    assert response.status_code == 422
    assert "Estoque insuficiente" in response.json()["detail"]


def test_invalid_transition_is_rejected(client, auth, catalog):
    order = open_order(client, auth, catalog)

    response = client.patch(
        f"/api/v1/orders/{order['id']}/status",
        headers=auth,
        json={"status": "DELIVERED"},
    )

    assert response.status_code == 422
    assert "Transição inválida" in response.json()["detail"]


def test_administrative_endpoints_require_authentication(client):
    assert client.get("/api/v1/orders").status_code == 401
    assert client.post("/api/v1/clients", json={}).status_code == 401


def test_order_status_is_publicly_available(client, auth, catalog):
    order = open_order(client, auth, catalog)

    response = client.get(f"/api/v1/orders/{order['id']}")

    assert response.status_code == 200
    assert response.json()["status"] == "RECEIVED"


def test_unknown_order_returns_not_found(client):
    response = client.get("/api/v1/orders/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
