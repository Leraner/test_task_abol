from pydantic import BaseModel
import datetime
import uuid


class ImageSchemaResponse(BaseModel):
    id: uuid.UUID
    name: str
    file_path: str
    upload_date: datetime.datetime
    resolution: str
    size: int


class ImagesSchemaResponse(BaseModel):
    images: list[ImageSchemaResponse]


class UpdateImagesSchema(BaseModel):
    name: str | None = None


class PaginatedImagesSchemaResponse(BaseModel):
    has_next_page: bool = False
    has_previous_page: bool = False
    total_count: int
    total_pages: int
    page: int
    items: list[ImageSchemaResponse]
