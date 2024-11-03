from pydantic import BaseModel, computed_field, model_validator
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
