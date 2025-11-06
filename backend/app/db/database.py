# backend/app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import Generator

# Cria a conexão com o banco usando a URL
engine = create_engine(settings.DATABASE_URL)

# Cria uma sessão para executar queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que todos os modelos vão herdar (Antiga base.py)
Base = declarative_base()

# Dependência para as rotas
def get_db() -> Generator:
    """Função de dependência que fornece a sessão do banco de dados (DB)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()