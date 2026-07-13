from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from app.domain.models import OSStatus

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    username: str
    password: str

class ClienteBase(BaseModel):
    nome: str
    documento: str
    telefone: str | None = None
    email: EmailStr | None = None
    @field_validator("documento")
    @classmethod
    def validar_documento(cls, v: str):
        numeros = re.sub(r"\D", "", v)
        if len(numeros) not in (11, 14):
            raise ValueError("CPF/CNPJ deve conter 11 ou 14 dígitos")
        return v
class ClienteCreate(ClienteBase): pass
class ClienteOut(ClienteBase):
    id: int
    class Config: from_attributes = True

class VeiculoBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    ano: int = Field(ge=1900, le=2100)
    cliente_id: int
    @field_validator("placa")
    @classmethod
    def validar_placa(cls, v: str):
        placa = v.upper().replace("-", "")
        if not re.match(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$", placa):
            raise ValueError("Placa inválida")
        return placa
class VeiculoCreate(VeiculoBase): pass
class VeiculoOut(VeiculoBase):
    id: int
    class Config: from_attributes = True

class ServicoBase(BaseModel):
    nome: str
    descricao: str | None = None
    preco: float = Field(gt=0)
    tempo_estimado_minutos: int = Field(gt=0)
class ServicoCreate(ServicoBase): pass
class ServicoOut(ServicoBase):
    id: int
    class Config: from_attributes = True

class PecaBase(BaseModel):
    nome: str
    codigo: str
    preco: float = Field(gt=0)
    quantidade_estoque: int = Field(ge=0)
class PecaCreate(PecaBase): pass
class PecaOut(PecaBase):
    id: int
    class Config: from_attributes = True

class ItemPecaOS(BaseModel):
    peca_id: int
    quantidade: int = Field(gt=0)
class OrdemServicoCreate(BaseModel):
    cliente_id: int
    veiculo_id: int
    servicos_ids: list[int]
    pecas: list[ItemPecaOS] = []
    observacao: str | None = None
class OrdemServicoStatusUpdate(BaseModel):
    status: OSStatus
class OrdemServicoOut(BaseModel):
    id: int
    cliente_id: int
    veiculo_id: int
    status: OSStatus
    observacao: str | None
    valor_total: float
    criada_em: datetime
    iniciada_em: datetime | None
    finalizada_em: datetime | None
    class Config: from_attributes = True
