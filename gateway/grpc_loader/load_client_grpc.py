from typing import Any, Callable
from .interceptors import KeyAuthClientInterceptor, KeyAuthClientInterceptorStreamUnary
from pydantic import BaseModel
import grpc


class ClientInterface:
    client: Any
    protos: Any


class GRPCLoaderContext(BaseModel):
    access_token: str | None = None
    stream_unary_access_token: str | None = None


class ClientGRPCLoader(type):
    __attrs = {}

    def __new__(cls, name: str, bases: tuple, dct: dict) -> type:
        cls.__attrs |= {
            "address": dct.get("address", None),
            "path_to_proto": dct.get("path_to_proto", None),
        }

        if any(map(lambda x: cls.__attrs[x], cls.__attrs)) is None:
            raise Exception("Missing required attributes")

        for method_name, method in dct.items():
            if callable(method):
                dct[method_name] = cls.load_client(
                    method, cls.__attrs["address"], cls.__attrs["path_to_proto"]
                )
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def annotate(func) -> Callable:
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    @staticmethod
    def load_client(func, address: str, path_to_proto: str):
        async def inner(*args, **kwargs):
            interceptors = []
            context: GRPCLoaderContext | None = next(
                filter(
                    lambda var: isinstance(var, GRPCLoaderContext),
                    [*kwargs.values(), *args],
                ),
                None,
            )

            if context is not None:
                if context.access_token is not None:
                    interceptors.append(KeyAuthClientInterceptor(context.access_token))

                if context.stream_unary_access_token is not None:
                    interceptors.append(
                        KeyAuthClientInterceptorStreamUnary(
                            context.stream_unary_access_token
                        )
                    )

            async with grpc.aio.insecure_channel(
                address, interceptors=interceptors
            ) as channel:
                protos, services = grpc.protos_and_services(path_to_proto)  # type: ignore
                stub_service_name = next(
                    filter(lambda x: "Stub" in x, services.__dict__)
                )
                client = services.__dict__[stub_service_name](channel)

                client_and_protos_object = ClientInterface()
                client_and_protos_object.__dict__.update(
                    {"client": client, "protos": protos}
                )
                result = await func(*args, **kwargs, interface=client_and_protos_object)
            return result

        return inner
