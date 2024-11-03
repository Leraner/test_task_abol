import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TIMEZONE = "Europe/Moscow"

RABBITMQ_BROKER_URL = "amqp://guest:guest@localhost/"

DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")  # "database"
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_DIALECT = os.getenv("DB_DIALECT", "postgresql")
DB_DRIVER = os.getenv("DB_DRIVER", "asyncpg")


PORT = os.getenv("PORT", "50050")
HOST = os.getenv("HOST", "0.0.0.0")


DATABASE_URL = (
    f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

BASE_DIR_MEDIA = Path("media")

FILES = {"images": BASE_DIR_MEDIA / "images/"}

IMAGE_UPLOAD_SIZES = [
    (100, 100),
    (500, 500),
]

AVAIlABLE_CONTENT_TYPES = (
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/tiff",
    "image/webp",
    "image/ico",
)


LOG_LEVEL = "DEBUG"
ERROR_LOG_PATH = "logs/error_logs"
LOG_PATH = "logs/other_logs"
