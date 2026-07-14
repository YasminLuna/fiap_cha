from itertools import count

_sequence = count(1)


def client_payload(**overrides):
    number = next(_sequence)
    payload = {
        "name": f"Cliente Teste {number}",
        "document": f"{10000000000 + number}",
        "email": f"cliente{number}@example.com",
        "phone": "81999999999",
    }
    payload.update(overrides)
    return payload


def vehicle_payload(client_id: str, **overrides):
    number = next(_sequence)
    letter = chr(65 + (number % 26))
    payload = {
        "client_id": client_id,
        "plate": f"TST{number % 10}{letter}{number % 10}{(number + 1) % 10}",
        "brand": "Honda",
        "model": "HR-V",
        "year": 2026,
    }
    payload.update(overrides)
    return payload


def service_payload(**overrides):
    number = next(_sequence)
    payload = {
        "name": f"Serviço {number}",
        "description": "Serviço criado para testes automatizados",
        "price": "180.00",
        "estimated_minutes": 45,
    }
    payload.update(overrides)
    return payload


def part_payload(**overrides):
    number = next(_sequence)
    payload = {
        "name": f"Peça {number}",
        "sku": f"SKU-{number:04d}",
        "price": "45.00",
        "stock": 10,
        "minimum_stock": 2,
    }
    payload.update(overrides)
    return payload


def order_payload(client_id: str, vehicle_id: str, service_ids: list[str], **overrides):
    payload = {
        "client_id": client_id,
        "vehicle_id": vehicle_id,
        "service_ids": service_ids,
        "parts": {},
        "notes": "Ordem criada em teste automatizado",
    }
    payload.update(overrides)
    return payload
