RABBITMQ_BROKER_URL = "amqp://guest:guest@rabbitmq/"

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
