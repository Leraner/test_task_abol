import uuid
from typing import Iterable

from .schemas import UpdateImagesSchema
import settings
from fastapi import UploadFile
from grpc_loader import ClientGRPCLoader, ClientInterface


class ImageProcessorController(metaclass=ClientGRPCLoader):
    address: str = settings.microservices["image_processor"]["address"]
    path_to_proto: str = settings.microservices["image_processor"]["path_to_proto"]

    @ClientGRPCLoader.annotate
    async def upload_file(self, file: UploadFile, interface: ClientInterface):
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

    @ClientGRPCLoader.annotate
    async def get_images(self, interface: ClientInterface):
        response = await interface.client.GetImages(
            interface.protos.GetImagesRequest(),
            timeout=5,
        )
        return response

    @ClientGRPCLoader.annotate
    async def get_image(self, image_id: uuid.UUID, interface: ClientInterface):
        response = await interface.client.GetImage(
            interface.protos.GetImageRequest(image_id=str(image_id)),
            timeout=5,
        )
        return response

    @ClientGRPCLoader.annotate
    async def delete_images(
        self, all_: bool, images_ids: list[uuid.UUID], interface: ClientInterface
    ):
        response = await interface.client.DeleteImages(
            interface.protos.DeleteImagesRequest(
                all_=all_,
                images_ids=[str(image_id) for image_id in images_ids],
            ),
            timeout=5,
        )
        return response

    @ClientGRPCLoader.annotate
    async def update_images(
        self,
        all_: bool,
        images_ids: list[uuid.UUID],
        update_schema: UpdateImagesSchema,
        interface: ClientInterface,
    ):
        response = await interface.client.UpdateImages(
            interface.protos.UpdateImagesRequest(
                all_=all_,
                images_ids=[str(image_id) for image_id in images_ids],
                update_schema=update_schema.model_dump_json(exclude_unset=True),
            )
        )

        return response
