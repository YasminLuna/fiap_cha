from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash

from .config import get_settings

bearer = HTTPBearer(auto_error=False)
password_hash = PasswordHash.recommended()


def create_token(subject: str) -> str:
    cfg = get_settings()
    exp = datetime.now(UTC) + timedelta(minutes=cfg.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": exp}, cfg.jwt_secret, algorithm="HS256")


def authenticate(email: str, password: str) -> bool:
    cfg = get_settings()
    return email == cfg.admin_email and password == cfg.admin_password


def require_admin(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")
    try:
        payload = jwt.decode(
            credentials.credentials, get_settings().jwt_secret, algorithms=["HS256"]
        )
        return str(payload["sub"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        ) from exc
