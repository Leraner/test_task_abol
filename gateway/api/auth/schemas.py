from pydantic import BaseModel, EmailStr
import uuid


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchemaResponse(BaseModel):
    access_token: str


class RegisterUserSchemaResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr


class RegisterSchemaResponse(BaseModel):
    user: RegisterUserSchemaResponse
