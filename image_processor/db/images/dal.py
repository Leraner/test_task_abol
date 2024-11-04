import uuid
from typing import Sequence, Any, Tuple

from schemas import CreateImageSchema, UpdateImageSchema, DatabaseException
from sqlalchemy import select, delete, update, func, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ImageModel


class ImageDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_images(
        self, create_schemas: list[CreateImageSchema]
    ) -> Sequence[ImageModel]:

        new_images = [
            ImageModel(**create_schema.model_dump()) for create_schema in create_schemas
        ]

        try:

            self.db_session.add_all(new_images)
            await self.db_session.flush()

            for new_image in new_images:
                await self.db_session.refresh(new_image)

        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        return new_images

    async def get_paginated_images(
        self, page: int, size: int
    ) -> Sequence[Row[tuple[ImageModel, Any]]]:
        query = (
            select(ImageModel, func.count(ImageModel.id).over().label("count"))
            .group_by(ImageModel.id)
            .offset((page - 1) * size)
            .limit(size)
        )

        try:
            result = await self.db_session.execute(query)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        rows = result.fetchall()

        return rows

    async def get_images(
        self,
    ) -> Sequence[ImageModel]:

        query = select(ImageModel)

        try:
            result = await self.db_session.execute(query)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        rows = result.scalars().all()

        return rows

    async def get_image(self, image_id: uuid.UUID) -> ImageModel:
        query = select(ImageModel).where(ImageModel.id == image_id)

        try:
            result = await self.db_session.execute(query)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        row = result.scalar()

        if row is None:
            raise DatabaseException(f"Image with id: {image_id} not found")

        return row

    async def update_images(
        self, all_: bool, images_ids: list[uuid.UUID], update_schema: UpdateImageSchema
    ) -> Sequence[Row[tuple[ImageModel, Any]]]:
        subquery = (
            select(ImageModel)
            .where(
                ImageModel.id.not_in(images_ids)
                if all_
                else ImageModel.id.in_(images_ids)
            )
            .subquery()
        )

        values = update_schema.model_dump(exclude_unset=True)

        if values.get("name") is not None:
            values["file_path"] = func.replace(
                ImageModel.file_path, ImageModel.name, values["name"]
            )

        query = (
            update(ImageModel)
            .where(ImageModel.name == subquery.c.name)
            .values(**values)
            .returning(ImageModel, subquery.c.name)
        )

        try:
            result = await self.db_session.execute(query)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        rows = result.all()

        return rows

    async def delete_images(
        self, all_: bool, images_ids: list[uuid.UUID]
    ) -> Sequence[ImageModel]:

        subquery = (
            select(ImageModel)
            .where(
                ImageModel.id.not_in(images_ids)
                if all_
                else ImageModel.id.in_(images_ids)
            )
            .subquery()
        )

        query = (
            delete(ImageModel)
            .where(ImageModel.name == subquery.c.name)
            .returning(ImageModel)
        )

        try:
            result = await self.db_session.execute(query)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        rows = result.scalars().all()

        return rows
