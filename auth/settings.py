import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_DIALECT = os.getenv("DB_DIALECT", "postgresql")
DB_DRIVER = os.getenv("DB_DRIVER", "asyncpg")

PORT = os.getenv("AUTH_PORT", "50051")
HOST = os.getenv("AUTH_HOST", "0.0.0.0")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10))


DATABASE_URL = (
    f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

LOG_LEVEL = "DEBUG"
ERROR_LOG_PATH = "logs/error_logs"
LOG_PATH = "logs/other_logs"
