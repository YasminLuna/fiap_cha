from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.security import create_access_token, require_admin
from app.db.session import get_db
from app.domain.models import Cliente, OrdemServico, Peca, Servico, Veiculo
from app.schemas.schemas import (
    ClienteCreate, ClienteOut, Login, OrdemServicoCreate, OrdemServicoOut,
    OrdemServicoStatusUpdate, PecaCreate, PecaOut, ServicoCreate, ServicoOut,
    Token, VeiculoCreate, VeiculoOut,
)
from app.services.os_service import atualizar_status, criar_ordem_servico

router = APIRouter()

@router.post("/auth/login", response_model=Token, tags=["Autenticação"])
def login(payload: Login):
    if payload.username == "admin" and payload.password == "admin123":
        return {"access_token": create_access_token(payload.username), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/clientes", response_model=ClienteOut, tags=["Clientes"], dependencies=[Depends(require_admin)])
def criar_cliente(payload: ClienteCreate, db: Session = Depends(get_db)):
    cliente = Cliente(**payload.model_dump())
    db.add(cliente); db.commit(); db.refresh(cliente)
    return cliente

@router.get("/clientes", response_model=list[ClienteOut], tags=["Clientes"], dependencies=[Depends(require_admin)])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.post("/veiculos", response_model=VeiculoOut, tags=["Veículos"], dependencies=[Depends(require_admin)])
def criar_veiculo(payload: VeiculoCreate, db: Session = Depends(get_db)):
    veiculo = Veiculo(**payload.model_dump())
    db.add(veiculo); db.commit(); db.refresh(veiculo)
    return veiculo

@router.get("/veiculos", response_model=list[VeiculoOut], tags=["Veículos"], dependencies=[Depends(require_admin)])
def listar_veiculos(db: Session = Depends(get_db)):
    return db.query(Veiculo).all()

@router.post("/servicos", response_model=ServicoOut, tags=["Serviços"], dependencies=[Depends(require_admin)])
def criar_servico(payload: ServicoCreate, db: Session = Depends(get_db)):
    servico = Servico(**payload.model_dump())
    db.add(servico); db.commit(); db.refresh(servico)
    return servico

@router.get("/servicos", response_model=list[ServicoOut], tags=["Serviços"])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(Servico).all()

@router.post("/pecas", response_model=PecaOut, tags=["Peças"], dependencies=[Depends(require_admin)])
def criar_peca(payload: PecaCreate, db: Session = Depends(get_db)):
    peca = Peca(**payload.model_dump())
    db.add(peca); db.commit(); db.refresh(peca)
    return peca

@router.get("/pecas", response_model=list[PecaOut], tags=["Peças"], dependencies=[Depends(require_admin)])
def listar_pecas(db: Session = Depends(get_db)):
    return db.query(Peca).all()

@router.post("/ordens-servico", response_model=OrdemServicoOut, tags=["Ordens de Serviço"], dependencies=[Depends(require_admin)])
def criar_os(payload: OrdemServicoCreate, db: Session = Depends(get_db)):
    return criar_ordem_servico(db, payload)

@router.get("/ordens-servico", response_model=list[OrdemServicoOut], tags=["Ordens de Serviço"], dependencies=[Depends(require_admin)])
def listar_os(db: Session = Depends(get_db)):
    return db.query(OrdemServico).all()

@router.get("/ordens-servico/{ordem_id}", response_model=OrdemServicoOut, tags=["Ordens de Serviço"])
def detalhar_os(ordem_id: int, db: Session = Depends(get_db)):
    ordem = db.get(OrdemServico, ordem_id)
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    return ordem

@router.patch("/ordens-servico/{ordem_id}/status", response_model=OrdemServicoOut, tags=["Ordens de Serviço"], dependencies=[Depends(require_admin)])
def mudar_status(ordem_id: int, payload: OrdemServicoStatusUpdate, db: Session = Depends(get_db)):
    return atualizar_status(db, ordem_id, payload.status)

@router.get("/metricas/tempo-medio-execucao", tags=["Métricas"], dependencies=[Depends(require_admin)])
def tempo_medio_execucao(db: Session = Depends(get_db)):
    ordens = db.query(OrdemServico).filter(OrdemServico.iniciada_em.isnot(None), OrdemServico.finalizada_em.isnot(None)).all()
    if not ordens:
        return {"tempo_medio_minutos": 0, "ordens_consideradas": 0}
    minutos = [(o.finalizada_em - o.iniciada_em).total_seconds() / 60 for o in ordens]
    return {"tempo_medio_minutos": round(sum(minutos) / len(minutos), 2), "ordens_consideradas": len(ordens)}
