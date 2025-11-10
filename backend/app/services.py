from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
import boto3
import json

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:767397693643:cafe_teste"

AWS_REGION = "us-east-1"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY= ""
AWS_SESSION_TOKEN = ""

try:
    
    sns_client = boto3.client(
        'sns', 
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
except Exception as e:
    print(f"ERRO ao inicializar Boto3: {e}")
    sns_client = None
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
    
    def get_by_username(self, db: Session, username: str) -> Optional[models.Usuario]:
        
        return db.query(self.model).filter(self.model.nome_usuario == username).first()
    
    def authenticate(self, db: Session, username: str, password: str) -> Optional[models.Usuario]:
        usuario = self.get_by_username(db, username=username)
        
        if not usuario:
            return None 

        
        if usuario.senha != password: 
            return None 
            
        return usuario 

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
        
        
        itens_detalhados = []
        total_pedido = 0.0

        
        for item in pedido.itens:
            
            produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
            
            if not produto:
                
                print(f"Aviso: Produto ID {item.produto_id} não encontrado.")
                continue

            db_item = models.ItemPedido(
                pedido_id=db_pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade
            )
            db.add(db_item)
            
            preco_unitario = produto.preco
            subtotal = preco_unitario * item.quantidade
            total_pedido += subtotal
            
            itens_detalhados.append({
                "nome": produto.nome,
                "quantidade": item.quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": subtotal
            })

        db.commit()
        db.refresh(db_pedido)
        
        
        if sns_client and SNS_TOPIC_ARN != "arn:aws:sns:us-east-1:767397693643:cafe_teste":
            
            
            subject = f"Confirmação de Pedido #{db_pedido.id} da Cafeteria"
            
            message = (
                f"Novo Pedido Recebido! \n\n"
                f"Detalhes do Pedido #{db_pedido.id}:\n"
                f"Usuário ID: {db_pedido.usuario_id}\n"
                f"Criado em: {db_pedido.criado_em.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            
            
            for item in itens_detalhados:
                message += (
                    f"{item['nome']} (x{item['quantidade']})\n"
                    f"  Subtotal: R$ {item['subtotal']:.2f} (R$ {item['preco_unitario']:.2f}/un)\n"
                )

            message += (
                f" Preço Total: R$ {total_pedido:.2f}\n"
                
            )
            try:
                response = sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject=subject
                )
                print(f"Notificação SNS publicada para Pedido #{db_pedido.id}. MessageId: {response['MessageId']}")

            except Exception as e:
                
                print(f"ERRO ao publicar no SNS para o pedido {db_pedido.id}: {e}")
        
        return db_pedido



usuario_service = UsuarioService()
produto_service = ProdutoService()
pedido_service = PedidoService()
