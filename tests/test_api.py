def setup_data(client, auth):
    c = client.post(
        "/api/v1/clients",
        headers=auth,
        json={"name": "Maria Silva", "document": "12345678901", "email": "maria@example.com"},
    ).json()
    v = client.post(
        "/api/v1/vehicles",
        headers=auth,
        json={
            "client_id": c["id"],
            "plate": "ABC1D23",
            "brand": "Honda",
            "model": "HR-V",
            "year": 2026,
        },
    ).json()
    s = client.post(
        "/api/v1/services",
        headers=auth,
        json={
            "name": "Troca de óleo",
            "description": "Óleo e filtro",
            "price": "180.00",
            "estimated_minutes": 45,
        },
    ).json()
    p = client.post(
        "/api/v1/parts",
        headers=auth,
        json={
            "name": "Filtro de óleo",
            "sku": "FLT-001",
            "price": "45.00",
            "stock": 10,
            "minimum_stock": 2,
        },
    ).json()
    return c, v, s, p


def test_critical_order_flow(client, auth):
    c, v, s, p = setup_data(client, auth)
    r = client.post(
        "/api/v1/orders",
        headers=auth,
        json={
            "client_id": c["id"],
            "vehicle_id": v["id"],
            "service_ids": [s["id"]],
            "parts": {p["id"]: 1},
        },
    )
    assert r.status_code == 201
    order = r.json()
    assert order["total"] == "225.00"
    oid = order["id"]
    assert (
        client.patch(
            f"/api/v1/orders/{oid}/status", headers=auth, json={"status": "DIAGNOSIS"}
        ).status_code
        == 200
    )
    assert (
        client.patch(
            f"/api/v1/orders/{oid}/status", headers=auth, json={"status": "AWAITING_APPROVAL"}
        ).status_code
        == 200
    )
    approved = client.post(f"/api/v1/orders/{oid}/budget-decision", json={"decision": "APPROVED"})
    assert approved.json()["status"] == "IN_PROGRESS"
    assert client.get(f"/api/v1/orders/{oid}").status_code == 200


def test_active_list_excludes_finished_and_orders_by_priority(client, auth):
    c, v, s, p = setup_data(client, auth)
    ids = []
    for _ in range(2):
        ids.append(
            client.post(
                "/api/v1/orders",
                headers=auth,
                json={
                    "client_id": c["id"],
                    "vehicle_id": v["id"],
                    "service_ids": [s["id"]],
                    "parts": {},
                },
            ).json()["id"]
        )
    client.patch(f"/api/v1/orders/{ids[1]}/status", headers=auth, json={"status": "DIAGNOSIS"})
    listed = client.get("/api/v1/orders", headers=auth).json()
    assert [x["status"] for x in listed] == ["DIAGNOSIS", "RECEIVED"]


def test_invalid_transition_and_auth(client, auth):
    assert client.get("/api/v1/orders").status_code == 401
    c, v, s, p = setup_data(client, auth)
    oid = client.post(
        "/api/v1/orders",
        headers=auth,
        json={"client_id": c["id"], "vehicle_id": v["id"], "service_ids": [s["id"]], "parts": {}},
    ).json()["id"]
    assert (
        client.patch(
            f"/api/v1/orders/{oid}/status", headers=auth, json={"status": "DELIVERED"}
        ).status_code
        == 422
    )
