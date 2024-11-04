from pydantic import BaseModel, computed_field, model_validator
from ..exceptions import ValidationException
import settings
import uuid


class CreateImageSchema(BaseModel):
    name: str
    file_path: str
    resolution: str
    size: int


class ImageIdsSchema(BaseModel):
    all_: bool = False
    images_ids: list[uuid.UUID]


class ImageIdSchema(BaseModel):
    image_id: uuid.UUID


class UpdateImageSchema(BaseModel):
    name: str | None = None

    @model_validator(mode="after")
    def validate_name(self):
        if self.name is None:
            return self

        name: list[str] = self.name.split(".")

        if len(name) > 2:
            raise ValidationException(
                "Неправильное имя файла. Пример: file_name.png/file_name"
            )

        self.name = name[0]

        return self
