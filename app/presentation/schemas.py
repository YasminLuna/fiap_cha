from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums import BudgetDecision, OrderStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Login(BaseModel):
    email: EmailStr
    password: str


class ClientCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    document: str
    email: EmailStr
    phone: str | None = None


class ClientOut(ClientCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    active: bool


class VehicleCreate(BaseModel):
    client_id: str
    plate: str
    brand: str
    model: str
    year: int = Field(ge=1900, le=2100)


class VehicleOut(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    active: bool


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal = Field(gt=0)
    estimated_minutes: int = Field(gt=0)


class ServiceOut(ServiceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    active: bool


class PartCreate(BaseModel):
    name: str
    sku: str
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    minimum_stock: int = Field(ge=0, default=0)


class PartOut(PartCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    active: bool


class OrderOpen(BaseModel):
    client_id: str
    vehicle_id: str
    service_ids: list[str] = Field(min_length=1)
    parts: dict[str, int] = Field(default_factory=dict, description="Mapa part_id: quantidade")
    notes: str | None = None


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    item_type: str
    reference_id: str
    description: str
    quantity: int
    unit_price: Decimal


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    client_id: str
    vehicle_id: str
    status: OrderStatus
    notes: str | None
    total: Decimal
    budget_approved: bool | None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemOut]


class StatusUpdate(BaseModel):
    status: OrderStatus


class BudgetWebhook(BaseModel):
    decision: BudgetDecision
    external_reference: str | None = None
