from sqlalchemy.ext.asyncio import AsyncSession

from .dal import ImageDAL
import uuid
from ..database_conn import DatabaseConnection
from schemas import (
    CreateImageSchema,
    ImageDbSchema,
    UpdateImageSchema,
    UpdatedImageDbSchema,
    PaginatedImagesSchema,
)
from ..utils import Pagination


class ImageHandler(Pagination):
    @DatabaseConnection.create_session
    async def create_images_database(
        self, create_schemas: list[CreateImageSchema], db_session: AsyncSession
    ) -> list[ImageDbSchema]:
        image_dal = ImageDAL(db_session)
        created_images = await image_dal.create_images(create_schemas)
        return [
            ImageDbSchema.model_validate(created_image)
            for created_image in created_images
        ]

    @DatabaseConnection.create_session
    async def get_images_database(
        self, db_session: AsyncSession
    ) -> list[ImageDbSchema]:
        image_dal = ImageDAL(db_session)
        fetched_images = await image_dal.get_images()
        return [ImageDbSchema.model_validate(image) for image in fetched_images]

    @DatabaseConnection.create_session
    async def get_paginated_images_database(
        self, page: int, size: int, db_session: AsyncSession
    ) -> PaginatedImagesSchema:
        image_dal = ImageDAL(db_session)
        fetched_images = await image_dal.get_paginated_images(page=page, size=size)
        total_count = fetched_images[0][1] if fetched_images else 0
        images = [ImageDbSchema.model_validate(image[0]) for image in fetched_images]
        return self.get_paginated_data(
            page=page,
            size=size,
            total_count=total_count,
            objects=images,
            model=PaginatedImagesSchema,
        )

    @DatabaseConnection.create_session
    async def get_image_database(
        self, image_id: uuid.UUID, db_session: AsyncSession
    ) -> ImageDbSchema:
        image_dal = ImageDAL(db_session)
        fetched_image = await image_dal.get_image(image_id)
        return ImageDbSchema.model_validate(fetched_image)

    @DatabaseConnection.create_session
    async def delete_images_database(
        self,
        images_ids: list[uuid.UUID],
        db_session: AsyncSession,
        all_: bool = False,
    ) -> list[ImageDbSchema]:
        image_dal = ImageDAL(db_session)
        deleted_images = await image_dal.delete_images(all_=all_, images_ids=images_ids)
        return [ImageDbSchema.model_validate(image) for image in deleted_images]

    @DatabaseConnection.create_session
    async def update_images_database(
        self,
        images_ids: list[uuid.UUID],
        update_schema: UpdateImageSchema,
        db_session: AsyncSession,
        all_: bool = False,
    ) -> list[ImageDbSchema]:
        image_dal = ImageDAL(db_session)
        updated_images = await image_dal.update_images(
            all_=all_, images_ids=images_ids, update_schema=update_schema
        )

        return [
            UpdatedImageDbSchema.model_validate(
                image[0], context={"_old_name": image[1]}
            )
            for image in updated_images
        ]
