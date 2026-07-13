from fastapi import FastAPI
from app.api.routes import router
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Integrado de Oficina Mecânica",
    description="MVP back-end para gestão de clientes, veículos, peças, serviços e ordens de serviço.",
    version="1.0.0",
)
app.include_router(router)

@app.get("/health", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok"}
