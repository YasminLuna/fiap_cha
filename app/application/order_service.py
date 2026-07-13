from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import case, select
from sqlalchemy.orm import Session

from app.domain.enums import BudgetDecision, OrderStatus
from app.domain.rules import DomainError, ensure_transition
from app.infrastructure.models import (
    ClientModel,
    OrderItemModel,
    OrderModel,
    PartModel,
    ServiceModel,
    VehicleModel,
)
from app.infrastructure.notifier import notify_status

PRIORITY = {
    OrderStatus.IN_PROGRESS.value: 1,
    OrderStatus.AWAITING_APPROVAL.value: 2,
    OrderStatus.DIAGNOSIS.value: 3,
    OrderStatus.RECEIVED.value: 4,
}


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def open(self, data):
        client = self.db.get(ClientModel, data.client_id)
        vehicle = self.db.get(VehicleModel, data.vehicle_id)
        if not client or not client.active:
            raise DomainError("Cliente não encontrado")
        if not vehicle or not vehicle.active or vehicle.client_id != client.id:
            raise DomainError("Veículo não pertence ao cliente")
        services = list(
            self.db.scalars(
                select(ServiceModel).where(
                    ServiceModel.id.in_(data.service_ids), ServiceModel.active.is_(True)
                )
            )
        )
        if len(services) != len(set(data.service_ids)):
            raise DomainError("Serviço inválido ou inativo")
        order = OrderModel(
            client_id=client.id,
            vehicle_id=vehicle.id,
            notes=data.notes,
            status=OrderStatus.RECEIVED.value,
        )
        total = Decimal("0")
        for service in services:
            order.items.append(
                OrderItemModel(
                    item_type="SERVICE",
                    reference_id=service.id,
                    description=service.name,
                    quantity=1,
                    unit_price=service.price,
                )
            )
            total += service.price
        for part_id, quantity in data.parts.items():
            if quantity <= 0:
                raise DomainError("Quantidade de peça deve ser positiva")
            part = self.db.get(PartModel, part_id)
            if not part or not part.active:
                raise DomainError("Peça inválida ou inativa")
            if part.stock < quantity:
                raise DomainError(f"Estoque insuficiente para {part.name}")
            part.stock -= quantity
            order.items.append(
                OrderItemModel(
                    item_type="PART",
                    reference_id=part.id,
                    description=part.name,
                    quantity=quantity,
                    unit_price=part.price,
                )
            )
            total += part.price * quantity
        order.total = total
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get(self, order_id):
        order = self.db.get(OrderModel, order_id)
        if not order:
            raise DomainError("Ordem de serviço não encontrada")
        return order

    def list_active(self):
        priority = case(PRIORITY, value=OrderModel.status, else_=99)
        stmt = (
            select(OrderModel)
            .where(OrderModel.status.in_(list(PRIORITY)))
            .order_by(priority, OrderModel.created_at.asc())
        )
        return list(self.db.scalars(stmt).unique())

    def change_status(self, order_id, target: OrderStatus):
        order = self.get(order_id)
        ensure_transition(OrderStatus(order.status), target)
        order.status = target.value
        if target == OrderStatus.FINISHED:
            order.finished_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(order)
        client = self.db.get(ClientModel, order.client_id)
        notify_status(client.email, order.id, target.value)
        return order

    def decide_budget(self, order_id, decision: BudgetDecision):
        order = self.get(order_id)
        if OrderStatus(order.status) != OrderStatus.AWAITING_APPROVAL:
            raise DomainError("OS não está aguardando aprovação")
        order.budget_approved = decision == BudgetDecision.APPROVED
        target = OrderStatus.IN_PROGRESS if order.budget_approved else OrderStatus.CANCELLED
        ensure_transition(OrderStatus(order.status), target)
        order.status = target.value
        self.db.commit()
        self.db.refresh(order)
        client = self.db.get(ClientModel, order.client_id)
        notify_status(client.email, order.id, target.value)
        return order
