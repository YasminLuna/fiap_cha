from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.domain.models import OrdemServico, OrdemServicoPeca, OrdemServicoServico, Peca, Servico, OSStatus
from app.schemas.schemas import OrdemServicoCreate


def criar_ordem_servico(db: Session, payload: OrdemServicoCreate) -> OrdemServico:
    ordem = OrdemServico(
        cliente_id=payload.cliente_id,
        veiculo_id=payload.veiculo_id,
        status=OSStatus.AGUARDANDO_APROVACAO,
        observacao=payload.observacao,
    )
    total = 0.0
    for servico_id in payload.servicos_ids:
        servico = db.get(Servico, servico_id)
        if not servico:
            raise HTTPException(status_code=404, detail=f"Serviço {servico_id} não encontrado")
        ordem.servicos.append(OrdemServicoServico(servico_id=servico.id, preco=servico.preco))
        total += servico.preco
    for item in payload.pecas:
        peca = db.get(Peca, item.peca_id)
        if not peca:
            raise HTTPException(status_code=404, detail=f"Peça {item.peca_id} não encontrada")
        if peca.quantidade_estoque < item.quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {peca.nome}")
        peca.quantidade_estoque -= item.quantidade
        ordem.pecas.append(OrdemServicoPeca(peca_id=peca.id, quantidade=item.quantidade, preco_unitario=peca.preco))
        total += peca.preco * item.quantidade
    ordem.valor_total = total
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    return ordem


def atualizar_status(db: Session, ordem_id: int, status: OSStatus) -> OrdemServico:
    ordem = db.get(OrdemServico, ordem_id)
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    ordem.status = status
    if status == OSStatus.EM_EXECUCAO and not ordem.iniciada_em:
        ordem.iniciada_em = datetime.utcnow()
    if status == OSStatus.FINALIZADA:
        ordem.finalizada_em = datetime.utcnow()
    db.commit()
    db.refresh(ordem)
    return ordem
