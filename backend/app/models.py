from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base
import random
import string


def gerar_id():
    return ''.join(random.choices(string.digits, k=8))

# --- Usuário ---
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, default=gerar_id)
    nome_usuario = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)

    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete-orphan")


# --- Produto ---
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, default=gerar_id)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    preco = Column(Float, nullable=False)

    itens_pedido = relationship("ItemPedido", back_populates="produto", cascade="all, delete-orphan")


# --- Pedido ---
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True, default=gerar_id)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")


# --- Item do Pedido (associação N:N entre Pedido e Produto) ---
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True, default=gerar_id)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")
