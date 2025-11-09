from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Usuario ---
class UsuarioBase(BaseModel):
    nome_usuario: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

class UsuarioDetalheResponse(UsuarioResponse):
    pedidos: Optional[List["PedidoResponse"]] = []



# --- Produto ---
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        orm_mode = True


# --- Item do Pedido ---
class ItemPedidoBase(BaseModel):
    produto_id: int
    quantidade: int

class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoResponse(ItemPedidoBase):
    id: int
    produto: ProdutoResponse

    class Config:
        orm_mode = True


# --- Pedido ---
class PedidoBase(BaseModel):
    usuario_id: int

class PedidoCreate(PedidoBase):
    itens: List[ItemPedidoCreate]

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    criado_em: datetime
    itens: List[ItemPedidoResponse] = []

    class Config:
        orm_mode = True


# Para permitir referências circulares
UsuarioResponse.update_forward_refs()
PedidoResponse.update_forward_refs()
