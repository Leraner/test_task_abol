from .controllers import AuthController
from .schemas import (
    LoginSchema,
    RegisterSchema,
    LoginSchemaResponse,
    RegisterSchemaResponse,
)
from ..base import BaseRouter


class AuthRouter(BaseRouter):
    prefix = "/auth"
    tags = ["auth"]
    controller = AuthController()

    response_models = {
        "post_login": LoginSchemaResponse,
        "post_signup": RegisterSchemaResponse,
    }

    @classmethod
    async def post_login(cls, login_schema: LoginSchema):
        response = await cls.controller.login_user(login_schema)
        return cls.proto_to_basemodel(instance=response, model=LoginSchemaResponse)

    @classmethod
    async def post_signup(cls, register_schema: RegisterSchema):
        response = await cls.controller.register_user(register_schema)
        return cls.proto_to_basemodel(instance=response, model=RegisterSchemaResponse)
