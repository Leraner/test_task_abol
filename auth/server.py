import grpc

import settings
from controllers import AuthController
from protos import auth_protos_pb2_grpc
from utils import log


async def run_server():
    server = grpc.aio.server()

    auth_protos_pb2_grpc.add_AuthServicer_to_server(AuthController(), server)

    address = f"{settings.HOST}:{settings.PORT}"
    server.add_insecure_port(address)

    log.info(f"Microservice started on address: {address}")

    await server.start()
    await server.wait_for_termination()
