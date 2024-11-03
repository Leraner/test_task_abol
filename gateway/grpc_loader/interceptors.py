from typing import Callable

import grpc
from grpc.aio import ClientCallDetails
from grpc.aio._call import StreamUnaryCall
from grpc.aio._typing import RequestType, RequestIterableType


class KeyAuthClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, user_token: str) -> None:
        # Получаем токен пользователя
        self.user_token: str = user_token

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        # Добавляем токен в метаданные с ключом rpc-auth и отправляем запрос на сервер
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(("rpc-auth", self.user_token))
        new_details = grpc.aio.ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
            client_call_details.wait_for_ready,
        )
        response = await continuation(new_details, request)
        return response


class KeyAuthClientInterceptorStreamUnary(grpc.aio.StreamUnaryClientInterceptor):
    def __init__(self, user_token: str):
        self.user_token = user_token

    async def intercept_stream_unary(
        self,
        continuation: Callable[[ClientCallDetails, RequestType], StreamUnaryCall],
        client_call_details: ClientCallDetails,
        request_iterator: RequestIterableType,
    ) -> StreamUnaryCall:
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(("rpc-auth", self.user_token))
        new_details = grpc.aio.ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
            client_call_details.wait_for_ready,
        )
        response = await continuation(new_details, request_iterator)
        return response
