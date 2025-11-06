# backend/app/main.py
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Importa os módulos consolidados
from app.db.database import Base, engine, get_db
from app import schemas, services # services contem a logica crud
from app.core.config import settings 

# --- Inicialização da Aplicação ---

# Cria as tabelas automaticamente
# Importa todos os modelos para garantir que o Base.metadata saiba sobre eles
import app.models 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API da cafeteria para gerenciar produtos, pedidos e usuários",
    version=settings.VERSION
)

# Rota básica
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da Cafeteria!"}


# --- Controllers (Rotas) ---

router_v1 = APIRouter(prefix="/api/v1")

# Rota de teste simples (Ping)
@router_v1.get("/ping")
def ping():
    return {"message": "pong"}

# Rotas de Usuários
@router_v1.get("/users", response_model=list[schemas.UserResponse], tags=["Users"])
def list_users(db: Session = Depends(get_db)):
    return services.user_service.get_all(db)

@router_v1.post("/users", response_model=schemas.UserResponse, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.user_service.create(db, user)

# Rotas de Produtos
@router_v1.get("/products", response_model=list[schemas.ProductResponse], tags=["Products"])
def list_products(db: Session = Depends(get_db)):
    return services.product_service.get_all(db)

@router_v1.post("/products", response_model=schemas.ProductResponse, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return services.product_service.create(db, product)

@router_v1.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = services.product_service.delete(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}

# Rotas de Pedidos
@router_v1.get("/orders", response_model=list[schemas.OrderResponse], tags=["Orders"])
def list_orders(db: Session = Depends(get_db)):
    return services.order_service.get_all(db)

@router_v1.post("/orders", response_model=schemas.OrderResponse, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return services.order_service.create(db, order)

# Inclui todas as rotas
app.include_router(router_v1)