RABBITMQ_BROKER_URL = "amqp://guest:guest@localhost/"

microservices = {
    "image_processor": {
        # image_processor
        "address": "0.0.0.0:50050",
        "path_to_proto": "protos/images.proto",
    },
    "auth": {
        "address": "0.0.0.0:50051",
        "path_to_proto": "protos/auth_protos.proto",
    },
}
