from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db
from app import schemas, services  # services contém a lógica CRUD
from app.core.config import settings 
from fastapi.middleware.cors import CORSMiddleware

import app.models
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API da cafeteria para gerenciar produtos, pedidos e usuários",
    version=settings.VERSION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
)




@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da Cafeteria!"}



router_v1 = APIRouter(prefix="/api/v1")


@router_v1.get("/ping", tags=["Geral"])
def ping():
    return {"message": "pong"}


# --- Rotas de Usuários ---
@router_v1.get("/usuarios", response_model=list[schemas.UsuarioResponse], tags=["Usuários"])
def listar_usuarios(db: Session = Depends(get_db)):
    return services.usuario_service.get_all(db)

@router_v1.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioDetalheResponse, tags=["Usuários"])
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = services.usuario_service.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router_v1.post("/usuarios", response_model=schemas.UsuarioResponse, tags=["Usuários"])
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return services.usuario_service.create(db, usuario)

@router_v1.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse, tags=["Usuários"])
def atualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    atualizado = services.usuario_service.update(db, usuario_id, usuario.dict())
    if not atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return atualizado

@router_v1.delete("/usuarios/{usuario_id}", tags=["Usuários"])
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    sucesso = services.usuario_service.delete(db, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}

@router_v1.post("/login", response_model=schemas.UsuarioResponse, tags=["Autenticação"])
def login(form_data: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = services.usuario_service.authenticate(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return usuario

# --- Rotas de Produtos ---
@router_v1.get("/produtos", response_model=list[schemas.ProdutoResponse], tags=["Produtos"])
def listar_produtos(db: Session = Depends(get_db)):
    return services.produto_service.get_all(db)

@router_v1.post("/produtos", response_model=schemas.ProdutoResponse, tags=["Produtos"])
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return services.produto_service.create(db, produto)

@router_v1.delete("/produtos/{produto_id}", tags=["Produtos"])
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    sucesso = services.produto_service.delete(db, produto_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}


# --- Rotas de Pedidos ---
@router_v1.get("/pedidos", response_model=list[schemas.PedidoResponse], tags=["Pedidos"])
def listar_pedidos(db: Session = Depends(get_db)):
    return services.pedido_service.get_all(db)

@router_v1.post("/pedidos", response_model=schemas.PedidoResponse, tags=["Pedidos"])
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return services.pedido_service.create(db, pedido)


# Inclui todas as rotas
app.include_router(router_v1)
