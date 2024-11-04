import json
from typing import AsyncIterable

import json
from typing import AsyncIterable

import grpc
import settings
from db import ImageHandler
from protos import images_pb2, images_pb2_grpc
from schemas import (
    CreateImageSchema,
    ImageDbSchema,
    ImageIdsSchema,
    ImageIdSchema,
    UpdateImageSchema,
    LogicException,
    PaginatedImagesSchema,
    DatabaseException,
    ValidationException,
)
from utils import Converter

from .services import ProcessImageService


class ImageProcessorController(
    images_pb2_grpc.ImageProcessorServicer,
    Converter,
    ProcessImageService,
    ImageHandler,
):
    async def UploadImage(
        self,
        request_iterator: AsyncIterable[images_pb2.UploadImageRequest],
        context: grpc.aio.ServicerContext,
    ):
        try:
            buffer, metadata = await self.get_image_chunks(request_iterator)
        except LogicException as e:
            await context.abort(grpc.StatusCode.ABORTED, details=e.message)

        create_schemas = []
        processed_images: list[dict] = []

        for target_size in settings.IMAGE_UPLOAD_SIZES:
            processed_image = self.process_image(buffer, metadata, target_size)
            resolution = f"{target_size[0]}x{target_size[1]}"
            file_path = f'{settings.FILES["images"]}/{resolution}{metadata.name}'
            create_schema = CreateImageSchema(
                name=metadata.name,
                file_path=file_path,
                resolution=resolution,
                size=self.get_image_size(processed_image),
            )
            create_schemas.append(create_schema)
            processed_images.append({"image": processed_image, "file_path": file_path})

        try:
            uploaded_images: list[ImageDbSchema] = await self.create_images_database(
                create_schemas
            )
        except DatabaseException as e:
            await context.abort(grpc.StatusCode.ABORTED, details=e.message)

        for processed_image in processed_images:
            self.save_image(
                metadata=metadata,
                image=processed_image["image"],
                file_path=processed_image["file_path"],
            )

        return images_pb2.UploadImageResponse(
            images=[
                self.basemodel_to_proto(instance=image, proto_model=images_pb2.Image)
                for image in uploaded_images
            ],
        )

    async def GetImages(
        self, request: images_pb2.GetImagesRequest, context: grpc.aio.ServicerContext
    ) -> images_pb2.GetImagesResponse:
        try:
            paginated_images_db: PaginatedImagesSchema = (
                await self.get_paginated_images_database(
                    page=request.page, size=request.size
                )
            )
        except DatabaseException as e:
            await context.abort(grpc.StatusCode.ABORTED, details=e.message)

        return self.basemodel_to_proto(
            instance=paginated_images_db, proto_model=images_pb2.GetImagesResponse
        )

    async def GetImage(
        self, request: images_pb2.GetImagesRequest, context: grpc.aio.ServicerContext
    ) -> images_pb2.GetImageResponse:
        image_id_schema: ImageIdSchema = self.proto_to_basemodel(
            instance=request, model=ImageIdSchema
        )
        try:
            image_db: ImageDbSchema = await self.get_image_database(
                image_id=image_id_schema.image_id
            )
        except DatabaseException as _:
            await context.abort(
                grpc.StatusCode.NOT_FOUND, details="Не найдено такое изображение"
            )

        return images_pb2.GetImageResponse(
            image=self.basemodel_to_proto(
                instance=image_db, proto_model=images_pb2.Image
            )
        )

    async def DeleteImages(
        self, request: images_pb2.DeleteImagesRequest, context: grpc.aio.ServicerContext
    ) -> images_pb2.DeleteImagesResponse:

        image_ids_schema: ImageIdsSchema = self.proto_to_basemodel(
            instance=request, model=ImageIdsSchema
        )

        try:
            deleted_images_db = await self.delete_images_database(
                all_=image_ids_schema.all_,
                images_ids=image_ids_schema.images_ids,
            )
        except DatabaseException as e:
            await context.abort(grpc.StatusCode.ABORTED, details=e.message)

        proto_images = []

        for image in deleted_images_db:
            proto_images.append(
                self.basemodel_to_proto(instance=image, proto_model=images_pb2.Image)
            )
            self.delete_image(image.file_path)

        return images_pb2.DeleteImagesResponse(images=proto_images)

    async def UpdateImages(
        self, request: images_pb2.UpdateImagesRequest, context: grpc.aio.ServicerContext
    ) -> images_pb2.UpdateImagesResponse:
        image_id_schema: ImageIdSchema = self.proto_to_basemodel(
            instance=request, model=ImageIdSchema
        )
        try:
            update_schema = UpdateImageSchema(**json.loads(request.update_schema))
        except ValidationException as e:
            await context.abort(grpc.StatusCode.ABORTED, details=e.message)

        try:
            updated_images = await self.update_images_database(
                images_ids=[image_id_schema.image_id],
                update_schema=update_schema,
            )
        except DatabaseException as e:
            await context.abort(grpc.StatusCode.ABORTED, details=e.message)

        proto_images = []

        for image in updated_images:
            proto_images.append(
                self.basemodel_to_proto(instance=image, proto_model=images_pb2.Image)
            )
            if image._old_name:
                self.rename_images(old_name=image._old_name, new_name=image.name)

        return images_pb2.UpdateImagesResponse(images=proto_images)
