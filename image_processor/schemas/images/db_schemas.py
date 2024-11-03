from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, ConfigDict, PrivateAttr
import uuid
import datetime


class ImageDbSchema(BaseModel):
    id: uuid.UUID
    name: str
    file_path: str
    upload_date: datetime.datetime
    resolution: str
    size: int

    model_config = ConfigDict(from_attributes=True)


class UpdatedImageDbSchema(ImageDbSchema):
    _old_name: str = PrivateAttr(default=None)

    def model_post_init(self, __context: Any) -> None:
        if self.name != __context["_old_name"]:
            self._old_name = __context["_old_name"]
        return super().model_post_init(__context)
