import boto3
from app.core.config import settings

sns_client = boto3.client('sns', region_name='us-east-1')

def notify_new_order(order_id: int, user_id: int):
    """Envia notificação quando um pedido é criado"""
    try:
        message = f"Novo pedido #{order_id} do usuário {user_id}!"
        sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:767397693643:cafe_topico',
            Subject='Novo Pedido - Cafeteria',
            Message=message
        )
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")