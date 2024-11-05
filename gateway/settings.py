import os

from dotenv import load_dotenv

load_dotenv()

RABBITMQ_BROKER_URL = "amqp://guest:guest@rabbitmq/"

REDIS_HOST = "redis"
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

REDIS_EXPIRE_CACHE = 1000


GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", 8000))
GATEWAY_HOST = os.getenv("GATEWAY_HOST", "0.0.0.0")


microservices = {
    "image_processor": {
        "address": "image_processor:50050",
        "path_to_proto": "protos/images.proto",
    },
    "auth": {
        "address": "auth:50051",
        "path_to_proto": "protos/auth_protos.proto",
    },
}
