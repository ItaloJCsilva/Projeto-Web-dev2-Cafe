# backend/app/services.py
from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional

# Classe base para métodos comuns de CRUD (pode ser expandida)
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

# Services Específicos

class UserService(BaseService):
    def __init__(self):
        super().__init__(models.User)
    
    def create(self, db: Session, user: schemas.UserCreate) -> models.User:
        # A lógica de hash de senha iria aqui
        return super().create(db, user)

class ProductService(BaseService):
    def __init__(self):
        super().__init__(models.Product)

    def get_by_id(self, db: Session, product_id: int) -> Optional[models.Product]:
        return db.query(self.model).filter(self.model.id == product_id).first()

    def delete(self, db: Session, product_id: int) -> bool:
        obj = self.get_by_id(db, product_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

class OrderService(BaseService):
    def __init__(self):
        super().__init__(models.Order)

# Instâncias de Services
user_service = UserService()
product_service = ProductService()
order_service = OrderService()