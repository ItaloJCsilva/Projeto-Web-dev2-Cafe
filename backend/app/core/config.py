from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cafeteria API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/cafe_db"
    JWT_SECRET: str = "supersecret"  

    class Config:
        env_file = ".env"  


settings = Settings()
