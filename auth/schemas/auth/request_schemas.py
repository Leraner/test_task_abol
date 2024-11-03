from pydantic import BaseModel, EmailStr


class CreateUserSchemaRequest(BaseModel):
    email: EmailStr
    hashed_password: str


class LoginUserSchemaRequest(CreateUserSchemaRequest): ...
