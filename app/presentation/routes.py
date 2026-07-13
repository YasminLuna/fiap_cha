from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.application.order_service import OrderService
from app.domain.rules import DomainError, validate_document, validate_plate
from app.infrastructure.database import get_db
from app.infrastructure.models import ClientModel, PartModel, ServiceModel, VehicleModel
from app.infrastructure.security import authenticate, create_token, require_admin

from .schemas import (
    BudgetWebhook,
    ClientCreate,
    ClientOut,
    Login,
    OrderOpen,
    OrderOut,
    PartCreate,
    PartOut,
    ServiceCreate,
    ServiceOut,
    StatusUpdate,
    Token,
    VehicleCreate,
    VehicleOut,
)

router = APIRouter(prefix="/api/v1")


def domain_error(exc: Exception):
    return HTTPException(status_code=422, detail=str(exc))


@router.post("/auth/token", response_model=Token, tags=["Autenticação"])
def login(data: Login):
    if not authenticate(data.email, data.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return Token(access_token=create_token(data.email))


@router.post(
    "/clients",
    response_model=ClientOut,
    status_code=201,
    tags=["Clientes"],
    dependencies=[Depends(require_admin)],
)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    try:
        obj = ClientModel(
            **data.model_dump(exclude={"document"}), document=validate_document(data.document)
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except (DomainError, IntegrityError) as exc:
        db.rollback()
        raise domain_error(exc) from exc


@router.get(
    "/clients",
    response_model=list[ClientOut],
    tags=["Clientes"],
    dependencies=[Depends(require_admin)],
)
def list_clients(db: Session = Depends(get_db)):
    return list(db.scalars(select(ClientModel).where(ClientModel.active.is_(True))))


@router.post(
    "/vehicles",
    response_model=VehicleOut,
    status_code=201,
    tags=["Veículos"],
    dependencies=[Depends(require_admin)],
)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    try:
        obj = VehicleModel(**data.model_dump(exclude={"plate"}), plate=validate_plate(data.plate))
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except (DomainError, IntegrityError) as exc:
        db.rollback()
        raise domain_error(exc) from exc


@router.get(
    "/vehicles",
    response_model=list[VehicleOut],
    tags=["Veículos"],
    dependencies=[Depends(require_admin)],
)
def list_vehicles(db: Session = Depends(get_db)):
    return list(db.scalars(select(VehicleModel).where(VehicleModel.active.is_(True))))


@router.post(
    "/services",
    response_model=ServiceOut,
    status_code=201,
    tags=["Catálogo"],
    dependencies=[Depends(require_admin)],
)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    obj = ServiceModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/services", response_model=list[ServiceOut], tags=["Catálogo"])
def list_services(db: Session = Depends(get_db)):
    return list(db.scalars(select(ServiceModel).where(ServiceModel.active.is_(True))))


@router.post(
    "/parts",
    response_model=PartOut,
    status_code=201,
    tags=["Peças"],
    dependencies=[Depends(require_admin)],
)
def create_part(data: PartCreate, db: Session = Depends(get_db)):
    obj = PartModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get(
    "/parts", response_model=list[PartOut], tags=["Peças"], dependencies=[Depends(require_admin)]
)
def list_parts(db: Session = Depends(get_db)):
    return list(db.scalars(select(PartModel).where(PartModel.active.is_(True))))


@router.post(
    "/orders",
    response_model=OrderOut,
    status_code=201,
    tags=["Ordens de Serviço"],
    dependencies=[Depends(require_admin)],
)
def open_order(data: OrderOpen, db: Session = Depends(get_db)):
    try:
        return OrderService(db).open(data)
    except DomainError as exc:
        raise domain_error(exc) from exc


@router.get(
    "/orders",
    response_model=list[OrderOut],
    tags=["Ordens de Serviço"],
    dependencies=[Depends(require_admin)],
)
def list_orders(db: Session = Depends(get_db)):
    return OrderService(db).list_active()


@router.get("/orders/{order_id}", response_model=OrderOut, tags=["Ordens de Serviço"])
def get_order(order_id: str, db: Session = Depends(get_db)):
    try:
        return OrderService(db).get(order_id)
    except DomainError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch(
    "/orders/{order_id}/status",
    response_model=OrderOut,
    tags=["Ordens de Serviço"],
    dependencies=[Depends(require_admin)],
)
def update_status(order_id: str, data: StatusUpdate, db: Session = Depends(get_db)):
    try:
        return OrderService(db).change_status(order_id, data.status)
    except DomainError as exc:
        raise domain_error(exc) from exc


@router.post("/orders/{order_id}/budget-decision", response_model=OrderOut, tags=["Integrações"])
def budget_webhook(order_id: str, data: BudgetWebhook, db: Session = Depends(get_db)):
    try:
        return OrderService(db).decide_budget(order_id, data.decision)
    except DomainError as exc:
        raise domain_error(exc) from exc
