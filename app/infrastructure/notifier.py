import logging
import smtplib
from email.message import EmailMessage

from .config import get_settings

logger = logging.getLogger(__name__)


def notify_status(to_email: str, order_id: str, status: str) -> None:
    cfg = get_settings()
    if not cfg.smtp_host:
        logger.info("notification order=%s recipient=%s status=%s", order_id, to_email, status)
        return
    msg = EmailMessage()
    msg["Subject"] = f"Atualização da OS {order_id}"
    msg["From"] = cfg.smtp_from
    msg["To"] = to_email
    msg.set_content(f"A ordem de serviço {order_id} agora está no status {status}.")
    with smtplib.SMTP(cfg.smtp_host, cfg.smtp_port, timeout=10) as server:
        server.starttls()
        if cfg.smtp_user and cfg.smtp_password:
            server.login(cfg.smtp_user, cfg.smtp_password)
        server.send_message(msg)
