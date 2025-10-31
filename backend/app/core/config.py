# backend/app/core/config.py
from pydantic import BaseSettings

# Usamos Pydantic para ler variáveis de ambiente de forma segura e tipada
class Settings(BaseSettings):
    PROJECT_NAME: str = "Cafeteria API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/cafe_db"
    JWT_SECRET: str = "supersecret"  # será usada depois na autenticação

    class Config:
        env_file = ".env"  # lê as variáveis de ambiente de um arquivo .env

# Instância única de configurações
settings = Settings()
