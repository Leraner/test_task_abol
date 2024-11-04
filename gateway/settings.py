import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


RABBITMQ_BROKER_URL = "amqp://guest:guest@localhost/"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

REDIS_EXPIRE_CACHE = 1000

microservices = {
    "image_processor": {
        "address": "0.0.0.0:50050",
        "path_to_proto": "protos/images.proto",
    },
    "auth": {
        "address": "0.0.0.0:50051",
        "path_to_proto": "protos/auth_protos.proto",
    },
}
