from functools import partial

import grpc
import settings
from jose import jwt


class AuthInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, key):
        # При инициализации создаем атрибут _valid_metadata,
        # который будет хранить секретный ключ для валидации токена пользователя
        self._valid_metadata = key

    @staticmethod
    async def deny(_, context, details):
        # Функция, предназначенная для отправки сообщений пользователю при отработках ошибок в функции intercept_service
        await context.abort(grpc.StatusCode.UNAUTHENTICATED, details)

    async def intercept_service(self, continuation, handler_call_details: grpc.HandlerCallDetails):
        # Получаем кортеж, содержащий метаданные
        metadata = handler_call_details.invocation_metadata
        try:
            # Получаем токен из метаданных
            result = next(filter(lambda x: x.key == "rpc-auth", metadata))
            if jwt.decode(result.value, self._valid_metadata, algorithms=[settings.ALGORITHM]):
                return await continuation(handler_call_details)
        except StopIteration:
            return grpc.unary_unary_rpc_method_handler(
                partial(self.deny, details="Токен не найден")
            )
        except jwt.ExpiredSignatureError:
            return grpc.unary_unary_rpc_method_handler(
                partial(self.deny, details="Время жизни токена истекло")
            )
        except jwt.JWTError:
            return grpc.unary_unary_rpc_method_handler(
                partial(self.deny, details="Токен не валиден")
            )
