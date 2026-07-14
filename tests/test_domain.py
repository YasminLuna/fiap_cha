import pytest

from app.domain.enums import OrderStatus
from app.domain.rules import DomainError, ensure_transition, validate_document, validate_plate


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("123.456.789-01", "12345678901"),
        ("12.345.678/0001-90", "12345678000190"),
    ],
)
def test_validate_document_normalizes_valid_values(raw, expected):
    assert validate_document(raw) == expected


@pytest.mark.parametrize("invalid", ["", "11111111111", "123", "abcdefghijk"])
def test_validate_document_rejects_invalid_values(invalid):
    with pytest.raises(DomainError, match="CPF/CNPJ inválido"):
        validate_document(invalid)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("abc-1d23", "ABC1D23"), ("ABC1234", "ABC1234")],
)
def test_validate_plate_normalizes_valid_values(raw, expected):
    assert validate_plate(raw) == expected


@pytest.mark.parametrize("invalid", ["ABC", "ABCD123", "1234567", "ABC-12"])
def test_validate_plate_rejects_invalid_values(invalid):
    with pytest.raises(DomainError, match="Placa inválida"):
        validate_plate(invalid)


def test_status_transition_accepts_expected_flow():
    ensure_transition(OrderStatus.RECEIVED, OrderStatus.DIAGNOSIS)
    ensure_transition(OrderStatus.DIAGNOSIS, OrderStatus.AWAITING_APPROVAL)
    ensure_transition(OrderStatus.AWAITING_APPROVAL, OrderStatus.IN_PROGRESS)


def test_status_transition_rejects_skipped_steps():
    with pytest.raises(DomainError, match="Transição inválida"):
        ensure_transition(OrderStatus.RECEIVED, OrderStatus.DELIVERED)
