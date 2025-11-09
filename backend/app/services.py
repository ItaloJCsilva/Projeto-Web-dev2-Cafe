from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
from app.notificacao import notify_new_order



class BaseService:
    def __init__(self, model):
        self.model = model

    def get_all(self, db: Session) -> List:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: schemas.BaseModel):
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj




class UsuarioService(BaseService):
    def __init__(self):
        super().__init__(models.Usuario)
    
    def create(self, db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
        # Aqui você pode futuramente adicionar hash de senha
        return super().create(db, usuario)

    def get_by_id(self, db: Session, usuario_id: int):
        return db.query(self.model).filter(self.model.id == usuario_id).first()

    def update(self, db: Session, usuario_id: int, usuario_data: dict):
        usuario = self.get_by_id(db, usuario_id)
        if not usuario:
            return None
        for key, value in usuario_data.items():
            setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
        return usuario

    def delete(self, db: Session, usuario_id: int):
        usuario = self.get_by_id(db, usuario_id)
        if not usuario:
            return False
        db.delete(usuario)
        db.commit()
        return True



class ProdutoService(BaseService):
    def __init__(self):
        super().__init__(models.Produto)

    def get_by_id(self, db: Session, produto_id: int) -> Optional[models.Produto]:
        return db.query(self.model).filter(self.model.id == produto_id).first()

    def delete(self, db: Session, produto_id: int) -> bool:
        obj = self.get_by_id(db, produto_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False


class PedidoService(BaseService):
    def __init__(self):
        super().__init__(models.Pedido)

    def create(self, db: Session, pedido: schemas.PedidoCreate) -> models.Pedido:
        
        db_pedido = models.Pedido(usuario_id=pedido.usuario_id)
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)

        
        for item in pedido.itens:
            db_item = models.ItemPedido(
                pedido_id=db_pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade
            )
            db.add(db_item)
        db.commit()
        db.refresh(db_pedido)

        

        return db_pedido



usuario_service = UsuarioService()
produto_service = ProdutoService()
pedido_service = PedidoService()
