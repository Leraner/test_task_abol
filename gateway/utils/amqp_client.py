import asyncio
from typing import Self
import aio_pika
import settings
from .singleton import SingletonMeta


class AMQPClient(metaclass=SingletonMeta):
    async def init(self) -> Self:
        self.connection = await aio_pika.connect_robust(
            settings.RABBITMQ_BROKER_URL, loop=asyncio.get_event_loop()
        )

        return self

    async def event_producer(
        self,
        message: str,
        event_store: str = "logs",
    ) -> None:

        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(event_store)

            await channel.default_exchange.publish(
                aio_pika.Message(message.encode()), routing_key=queue.name
            )
