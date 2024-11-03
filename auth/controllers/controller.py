import grpc
from protos import auth_protos_pb2_grpc, auth_protos_pb2
from utils import Converter
from schemas import CreateUserSchemaRequest, DatabaseException
from .services import AuthService
from db import AuthHandlers
import datetime
import settings


class AuthController(
    auth_protos_pb2_grpc.AuthServicer,
    Converter,
    AuthService,
    AuthHandlers,
):
    async def Login(
        self, request: auth_protos_pb2.LoginRequest, context: grpc.aio.ServicerContext
    ) -> auth_protos_pb2.LoginResponse:

        user = await self.get_user_by_email(email=request.email)

        if user is None:
            await context.abort(
                grpc.StatusCode.NOT_FOUND, details="Неверный емэйл или пароль"
            )

        if not self.verify_password(request.password, user._hashed_password):
            await context.abort(
                grpc.StatusCode.NOT_FOUND, details="Неверный емэйл или пароль"
            )

        access_token_expires = datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return auth_protos_pb2.LoginResponse(access_token=access_token)

    async def SignUp(
        self, request: auth_protos_pb2.SignUpRequest, context: grpc.aio.ServicerContext
    ) -> auth_protos_pb2.SignUpResponse:
        user_data: dict = self.proto_to_dict(instance=request)
        user_data["hashed_password"] = self.get_password_hash(user_data.pop("password"))

        create_schema = CreateUserSchemaRequest(**user_data)

        try:
            created_user = await self.create_user(create_schema)
        except DatabaseException as _:
            await context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                details="Такой пользователь уже существует",
            )

        return auth_protos_pb2.SignUpResponse(
            user=self.basemodel_to_proto(
                instance=created_user, proto_model=auth_protos_pb2.User
            )
        )
