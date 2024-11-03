import asyncio
import uuid

from fastapi import UploadFile, Query, Depends
from starlette.responses import JSONResponse
from utils import AMQPClient

from .controllers import ImageProcessorController
from .schemas import ImagesSchemaResponse, ImageSchemaResponse, UpdateImagesSchema
from ..base import BaseRouter


class ImageProcessorRouter(BaseRouter):
    prefix = "/image"
    tags = ["image_processor"]
    controller = ImageProcessorController()

    paths = {
        "post_upload_image": "",
        "get_image": "/{image_id}/",
        "get_images": "",
        "delete_images": "",
        "patch_update_images": "",
    }

    response_models = {
        "get_images": ImagesSchemaResponse,
        "get_image": ImageSchemaResponse,
        "delete_images": ImagesSchemaResponse,
        "patch_update_images": ImagesSchemaResponse,
    }

    @classmethod
    async def post_upload_image(
        cls, file: UploadFile, amqp_client: AMQPClient = Depends(AMQPClient().init)
    ):
        asyncio.ensure_future(amqp_client.event_producer(message="Event: upload image"))
        response = await cls.controller.upload_file(file)
        return JSONResponse(cls.proto_to_dict(instance=response))

    @classmethod
    async def get_images(cls, amqp_client: AMQPClient = Depends(AMQPClient().init)):
        asyncio.ensure_future(
            amqp_client.event_producer(message="Event: get all images")
        )
        response = await cls.controller.get_images()
        return cls.proto_to_basemodel(instance=response, model=ImagesSchemaResponse)

    @classmethod
    async def get_image(
        cls, image_id: uuid.UUID, amqp_client: AMQPClient = Depends(AMQPClient().init)
    ):
        asyncio.ensure_future(
            amqp_client.event_producer(message=f"Event: get image by id {image_id}")
        )
        response = await cls.controller.get_image(image_id=image_id)
        return cls.proto_to_basemodel(
            instance=response.image, model=ImageSchemaResponse
        )

    @classmethod
    async def delete_images(
        cls,
        all_: bool = Query(default=False),
        images_ids: list[uuid.UUID] = Query(),
        amqp_client: AMQPClient = Depends(AMQPClient().init),
    ):
        asyncio.ensure_future(
            amqp_client.event_producer(
                message=f"Event: delete images with params: all_ = {all_}, images_ids = {images_ids}"
            )
        )
        response = await cls.controller.delete_images(all_=all_, images_ids=images_ids)
        return cls.proto_to_basemodel(instance=response, model=ImagesSchemaResponse)

    @classmethod
    async def patch_update_images(
        cls,
        update_schema: UpdateImagesSchema,
        all_: bool = Query(default=False),
        images_ids: list[uuid.UUID] = Query(),
        amqp_client: AMQPClient = Depends(AMQPClient().init),
    ):
        asyncio.ensure_future(
            amqp_client.event_producer(
                message=f"Event: Update images with params: all_ = {all_}, images_ids = {images_ids}"
            )
        )
        response = await cls.controller.update_images(
            all_=all_,
            images_ids=images_ids,
            update_schema=update_schema,
        )
        return cls.proto_to_basemodel(instance=response, model=ImagesSchemaResponse)

    @classmethod
    async def get_ping(cls):
        return JSONResponse({"ping": "pong"})
