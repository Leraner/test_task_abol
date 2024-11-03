import asyncio

import grpc

import settings
from controllers import ImageProcessorController
from management import Commands
from protos import images_pb2_grpc
from utils import AMQPServer, log


async def run_server():
    server = grpc.aio.server()

    amqp_client: AMQPServer = await AMQPServer().init()

    asyncio.ensure_future(
        amqp_client.event_consumer(amqp_client.async_wrapper(log.info))
    )

    commands = Commands()
    commands.create_default_folders()

    images_pb2_grpc.add_ImageProcessorServicer_to_server(
        ImageProcessorController(), server
    )

    address = f"{settings.HOST}:{settings.PORT}"
    server.add_insecure_port(address)

    log.info(f"Microservice started on address: {address}")

    await server.start()
    await server.wait_for_termination()
