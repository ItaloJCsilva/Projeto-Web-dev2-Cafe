# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Cria a conexão com o banco usando a URL do .env/config.py
engine = create_engine(settings.DATABASE_URL)

# Cria uma sessão para executar queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
