# backend/app/main.py
from fastapi import FastAPI
from app.api.v1.routers_ping import router as ping_router

# Cria uma instância do aplicativo FastAPI
app = FastAPI(
    title="Cafeteria API",
    description="API da cafeteria para gerenciar produtos, pedidos e usuários",
    version="1.0.0"
)

# Inclui as rotas de exemplo (ping)
app.include_router(ping_router, prefix="/api/v1", tags=["ping"])

# Endpoint raiz (teste rápido)
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da Cafeteria!"}
