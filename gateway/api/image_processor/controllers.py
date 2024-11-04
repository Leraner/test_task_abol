import uuid
from typing import Iterable

import grpc.aio
from utils import retry
from .schemas import UpdateImagesSchema
import settings
from fastapi import UploadFile
from grpc_loader import ClientGRPCLoader, ClientInterface, GRPCLoaderContext


class ImageProcessorController(metaclass=ClientGRPCLoader):
    address: str = settings.microservices["image_processor"]["address"]
    path_to_proto: str = settings.microservices["image_processor"]["path_to_proto"]

    @retry(exceptions=(grpc.aio.AioRpcError))
    @ClientGRPCLoader.annotate
    async def upload_file(
        self,
        file: UploadFile,
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        def generate_image_chunks(
            file: UploadFile, interface: ClientInterface
        ) -> Iterable:

            # Создаём чанки читая файл по 4 КБ
            for chunk in iter(lambda: file.file.read(4096), b""):
                request = interface.protos.UploadImageRequest(
                    meta=interface.protos.Metadata(
                        name=file.filename,
                        size=file.size,
                        content_type=file.headers.get("content-type", ""),
                    ),
                    image=chunk,
                )
                yield request

        response = await interface.client.UploadImage(
            generate_image_chunks(file, interface)
        )

        return response

    @retry(exceptions=(grpc.aio.AioRpcError))
    @ClientGRPCLoader.annotate
    async def get_images(
        self,
        page: int,
        size: int,
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        response = await interface.client.GetImages(
            interface.protos.GetImagesRequest(page=page, size=size),
            timeout=5,
        )
        return response

    @retry(exceptions=(grpc.aio.AioRpcError))
    @ClientGRPCLoader.annotate
    async def get_image(
        self,
        image_id: uuid.UUID,
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        response = await interface.client.GetImage(
            interface.protos.GetImageRequest(image_id=str(image_id)),
            timeout=5,
        )
        return response

    @retry(exceptions=(grpc.aio.AioRpcError))
    @ClientGRPCLoader.annotate
    async def delete_images(
        self,
        all_: bool,
        images_ids: list[uuid.UUID],
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        response = await interface.client.DeleteImages(
            interface.protos.DeleteImagesRequest(
                all_=all_,
                images_ids=[str(image_id) for image_id in images_ids],
            ),
            timeout=5,
        )
        return response

    @retry(exceptions=(grpc.aio.AioRpcError))
    @ClientGRPCLoader.annotate
    async def update_image(
        self,
        image_id: uuid.UUID,
        update_schema: UpdateImagesSchema,
        interface: ClientInterface,
        context: GRPCLoaderContext = GRPCLoaderContext(),
    ):
        response = await interface.client.UpdateImages(
            interface.protos.UpdateImagesRequest(
                image_id=str(image_id),
                update_schema=update_schema.model_dump_json(exclude_unset=True),
            )
        )

        return response
