import pytest
from pydantic import ValidationError
from app.schemas.schemas import ClienteCreate, VeiculoCreate


def test_cliente_documento_invalido():
    with pytest.raises(ValidationError):
        ClienteCreate(nome="Cliente Teste", documento="123", telefone="81999999999")


def test_veiculo_placa_mercosul_valida():
    veiculo = VeiculoCreate(placa="ABC1D23", marca="Jeep", modelo="Renegade", ano=2025, cliente_id=1)
    assert veiculo.placa == "ABC1D23"
