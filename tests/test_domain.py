import pytest

from app.domain.enums import OrderStatus
from app.domain.rules import DomainError, ensure_transition, validate_document, validate_plate


def test_validations():
    assert validate_document("123.456.789-01") == "12345678901"
    assert validate_plate("ABC-1D23") == "ABC1D23"
    with pytest.raises(DomainError):
        validate_document("111.111.111-11")
    with pytest.raises(DomainError):
        validate_plate("XPTO")


def test_status_transition():
    ensure_transition(OrderStatus.RECEIVED, OrderStatus.DIAGNOSIS)
    with pytest.raises(DomainError):
        ensure_transition(OrderStatus.RECEIVED, OrderStatus.DELIVERED)
