# backend/app/db/base.py
from sqlalchemy.orm import declarative_base

# Classe base que todos os modelos (User, Product, etc.) vão herdar
Base = declarative_base()
