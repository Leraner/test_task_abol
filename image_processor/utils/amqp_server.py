import asyncio
import aio_pika
import settings
from typing import Callable, Self
from functools import partial


class AMQPServer:
    async def init(self) -> Self:
        self.connection = await aio_pika.connect_robust(
            settings.RABBITMQ_BROKER_URL, loop=asyncio.get_event_loop()
        )
        return self

    async def event_consumer(
        self,
        callback: Callable,
        queue_name: str = "logs",
    ):
        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(queue_name)
            await queue.consume(partial(self._process_message, callback=callback))  # type: ignore
            await asyncio.Future()

    @staticmethod
    def async_wrapper(callback: Callable):
        async def inner(*args, **kwargs):
            return await asyncio.to_thread(callback, *args, **kwargs)

        return inner

    async def _process_message(
        self, message: aio_pika.IncomingMessage, callback: Callable
    ) -> None:
        async with message.process(ignore_processed=True):
            await message.ack()
            await callback(message.body.decode())
