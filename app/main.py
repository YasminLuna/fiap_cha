import time

from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import text

from app.infrastructure.config import get_settings
from app.infrastructure.database import Base, engine
from app.presentation.routes import router

REQUESTS = Counter("http_requests_total", "Total de requisições", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Latência HTTP", ["method", "path"])


def create_app() -> FastAPI:
    cfg = get_settings()
    Base.metadata.create_all(engine)
    app = FastAPI(
        title=cfg.app_name,
        version="2.0.0",
        description="Sistema de gestão de oficina mecânica — Tech Challenge Fase 2",
    )

    @app.middleware("http")
    async def metrics(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        path = request.url.path
        REQUESTS.labels(request.method, path, response.status_code).inc()
        LATENCY.labels(request.method, path).observe(time.perf_counter() - start)
        return response

    @app.get("/health", tags=["Operação"])
    def health():
        return {"status": "ok"}

    @app.get("/ready", tags=["Operação"])
    def ready():
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready"}

    @app.get("/metrics", include_in_schema=False)
    def metrics_endpoint():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    app.include_router(router)
    return app


app = create_app()
