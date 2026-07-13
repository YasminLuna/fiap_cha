import re

from .enums import OrderStatus


class DomainError(ValueError):
    pass


TRANSITIONS = {
    OrderStatus.RECEIVED: {OrderStatus.DIAGNOSIS},
    OrderStatus.DIAGNOSIS: {OrderStatus.AWAITING_APPROVAL},
    OrderStatus.AWAITING_APPROVAL: {OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED},
    OrderStatus.IN_PROGRESS: {OrderStatus.FINISHED},
    OrderStatus.FINISHED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}


def digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def validate_document(value: str) -> str:
    clean = digits(value)
    if len(clean) not in (11, 14) or len(set(clean)) == 1:
        raise DomainError("CPF/CNPJ inválido")
    return clean


def validate_plate(value: str) -> str:
    plate = re.sub(r"[^A-Za-z0-9]", "", value or "").upper()
    if not re.fullmatch(r"[A-Z]{3}[0-9][A-Z0-9][0-9]{2}", plate):
        raise DomainError("Placa inválida")
    return plate


def ensure_transition(current: OrderStatus, target: OrderStatus) -> None:
    if target not in TRANSITIONS[current]:
        raise DomainError(f"Transição inválida: {current} -> {target}")
