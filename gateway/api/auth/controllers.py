import settings
from grpc_loader import ClientGRPCLoader, ClientInterface, GRPCLoaderContext
from .schemas import LoginSchema, RegisterSchema


class AuthController(metaclass=ClientGRPCLoader):
    address: str = settings.microservices["auth"]["address"]
    path_to_proto: str = settings.microservices["auth"]["path_to_proto"]

    @ClientGRPCLoader.annotate
    async def login_user(
        self,
        login_schema: LoginSchema,
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        response = await interface.client.Login(
            interface.protos.LoginRequest(
                **login_schema.model_dump(mode="json"),
            ),
            timeout=5,
        )
        return response

    @ClientGRPCLoader.annotate
    async def register_user(
        self,
        register_schema: RegisterSchema,
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        response = await interface.client.SignUp(
            interface.protos.SignUpRequest(
                **register_schema.model_dump(mode="json"),
            ),
            timeout=5,
        )
        return response
