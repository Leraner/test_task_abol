import asyncio
from concurrent import futures

import grpc

import settings
from controllers import ImageProcessorController
from management import Commands
from protos import images_pb2_grpc
from utils import AMQPServer, log
from interceptors import AuthInterceptor


async def run_server():
    server = grpc.aio.server(
        interceptors=(AuthInterceptor(settings.SECRET_KEY),),
    )

    amqp_client: AMQPServer = await AMQPServer().init()

    commands = Commands()
    commands.create_default_folders()

    images_pb2_grpc.add_ImageProcessorServicer_to_server(
        ImageProcessorController(), server
    )

    address = f"{settings.HOST}:{settings.PORT}"
    server.add_insecure_port(address)

    log.info(f"Microservice started on address: {address}")

    await server.start()
    await asyncio.gather(
        amqp_client.event_consumer(amqp_client.async_wrapper(log.info)),
        server.wait_for_termination()
    )
