import os
from pydantic import BaseModel   



DB_USER = "root"
DB_PASSWORD = "Sandhya1997"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "vinfast_db"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SECRET_KEY = "vinfast-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "vinfast-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/vinfast"
    )


settings = Settings()