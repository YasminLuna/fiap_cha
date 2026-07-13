from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class OSStatus(str, Enum):
    RECEBIDA = "Recebida"
    EM_DIAGNOSTICO = "Em diagnóstico"
    AGUARDANDO_APROVACAO = "Aguardando aprovação"
    EM_EXECUCAO = "Em execução"
    FINALIZADA = "Finalizada"
    ENTREGUE = "Entregue"

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    documento = Column(String(18), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    veiculos = relationship("Veiculo", back_populates="cliente")

class Veiculo(Base):
    __tablename__ = "veiculos"
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(8), unique=True, nullable=False, index=True)
    marca = Column(String(80), nullable=False)
    modelo = Column(String(80), nullable=False)
    ano = Column(Integer, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    cliente = relationship("Cliente", back_populates="veiculos")

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    tempo_estimado_minutos = Column(Integer, nullable=False, default=60)

class Peca(Base):
    __tablename__ = "pecas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False, default=0)

class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    status = Column(SqlEnum(OSStatus), nullable=False, default=OSStatus.RECEBIDA)
    observacao = Column(Text, nullable=True)
    valor_total = Column(Float, nullable=False, default=0)
    criada_em = Column(DateTime, default=datetime.utcnow)
    iniciada_em = Column(DateTime, nullable=True)
    finalizada_em = Column(DateTime, nullable=True)
    cliente = relationship("Cliente")
    veiculo = relationship("Veiculo")
    servicos = relationship("OrdemServicoServico", cascade="all, delete-orphan")
    pecas = relationship("OrdemServicoPeca", cascade="all, delete-orphan")

class OrdemServicoServico(Base):
    __tablename__ = "ordem_servico_servicos"
    id = Column(Integer, primary_key=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    preco = Column(Float, nullable=False)
    servico = relationship("Servico")

class OrdemServicoPeca(Base):
    __tablename__ = "ordem_servico_pecas"
    id = Column(Integer, primary_key=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    peca_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    peca = relationship("Peca")
