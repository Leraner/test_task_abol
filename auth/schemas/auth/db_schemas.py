from typing import Any

from pydantic import BaseModel, EmailStr, PrivateAttr, ConfigDict
import uuid


class UserDbSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr

    _hashed_password: str = PrivateAttr(default="")

    model_config = ConfigDict(from_attributes=True)

    def model_post_init(self, __context: Any) -> None:
        self._hashed_password = __context["_hashed_password"]
        return super().model_post_init(__context)
