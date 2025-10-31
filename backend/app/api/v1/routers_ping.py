# backend/app/api/v1/routes_ping.py
from fastapi import APIRouter

# Cria um objeto 'router' para agrupar rotas relacionadas
router = APIRouter()

@router.get("/ping")
def ping():
    """
    Endpoint simples para testar se a API está viva.
    Acesse /api/v1/ping → deve retornar {"ping": "pong"}
    """
    return {"ping": "pong"}
