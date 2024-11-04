import glob
import io
import os
import uuid
from typing import Iterable

import pytest
from schemas.images.request_schemas import UpdateImageSchema
import settings
from PIL import Image
from google.protobuf.json_format import MessageToDict
from protos import images_pb2


class ImageService:
    def proto_to_dict(self, response):
        return MessageToDict(
            message=response,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )


class TestImages(ImageService):
    async def test_upload_images(self, grpc_client):
        image_data = {"name": "image1.png", "size": 123321, "content_type": "image/png"}

        def generate_image_chunks(
            file: io.BytesIO, content_type: str, size: int, name: str
        ) -> Iterable:
            # Создаём чанки читая файл по 4 КБ
            for chunk in iter(lambda: file.read(4096), b""):
                request = images_pb2.UploadImageRequest(
                    meta=images_pb2.Metadata(
                        name=name,
                        size=size,
                        content_type=content_type,
                    ),
                    image=chunk,
                )
                yield request

        file = io.BytesIO()

        image = Image.open("tests/resources/image1.png")
        image.save(file, format="PNG")

        file.seek(0)

        files_in_path: list[str] = glob.glob(f"{settings.FILES['images']}/*.*")

        assert len(files_in_path) == 0

        response: images_pb2.UploadImageResponse = await grpc_client.UploadImage(
            generate_image_chunks(file, **image_data)
        )

        response_dict: dict = self.proto_to_dict(response)

        for image in response_dict["images"]:
            assert image["name"] == "image1.png"
            assert str(settings.FILES["images"]) in image["file_path"]

        files_in_path: list[str] = glob.glob(f"{settings.FILES['images']}/*.*")

        assert len(files_in_path) == 2

    @pytest.mark.parametrize(
        "delete_params",
        [
            {"all_": False, "need_id": False},
            {"all_": False, "need_id": True},
            {"all_": True, "need_id": True},
            {"all_": True, "need_id": False},
        ],
    )
    async def test_delete_images(
        self,
        grpc_client,
        create_image_in_database,
        get_all_images_from_database,
        delete_params: dict,
    ):
        images_data: list[dict] = [
            {
                "image_id": uuid.uuid4(),
                "name": f"image{image_count}.png",
                "file_path": f"{settings.FILES['images']}/{resolution[0]}x{resolution[1]}image{image_count}.png",
                "resolution": f"{resolution[0]}x{resolution[1]}",
                "size": 123,
            }
            for resolution in settings.IMAGE_UPLOAD_SIZES
            for image_count in range(3)
        ]

        for image_data in images_data:
            await create_image_in_database(**image_data)

        files_in_path: list[str] = glob.glob(f"{settings.FILES['images']}/*.*")

        assert len(files_in_path) == 6

        response: images_pb2.DeleteImagesResponse = await grpc_client.DeleteImages(
            images_pb2.DeleteImagesRequest(
                all_=delete_params["all_"],
                images_ids=(
                    [str(images_data[0]["image_id"])]
                    if delete_params["need_id"]
                    else []
                ),
            )
        )

        response_dict: dict = self.proto_to_dict(response)

        images_from_database = await get_all_images_from_database()

        files_in_path: list[str] = glob.glob(f"{settings.FILES['images']}/*.*")

        if delete_params["all_"] is False and delete_params["need_id"] is False:
            assert response_dict["images"] == []
            assert len(files_in_path) == 6
            assert len(images_from_database) == 6

        if delete_params["all_"] is False and delete_params["need_id"] is True:
            files_in_path: list[str] = glob.glob(f"{settings.FILES['images']}/*.*")
            assert len(files_in_path) == 4
            assert len(images_from_database) == 4

        if delete_params["all_"] is True and delete_params["need_id"] is False:
            assert len(files_in_path) == 0
            assert len(images_from_database) == 0

        if delete_params["all_"] is True and delete_params["need_id"] is True:
            assert len(files_in_path) == 2
            assert len(images_from_database) == 2

    async def test_update_image(
        self, grpc_client, create_image_in_database, get_image_by_uuid_from_database
    ):
        name_for_update = "new_test_name.png"

        images_data: list[dict] = [
            {
                "image_id": uuid.uuid4(),
                "name": f"image{image_count}.png",
                "file_path": f"{settings.FILES['images']}/{resolution[0]}x{resolution[1]}image{image_count}.png",
                "resolution": f"{resolution[0]}x{resolution[1]}",
                "size": 123,
            }
            for resolution in settings.IMAGE_UPLOAD_SIZES
            for image_count in range(1)
        ]

        for image_data in images_data:
            await create_image_in_database(**image_data)

        files_in_path_before_update: list[str] = glob.glob(
            f"{settings.FILES['images']}/*.*"
        )

        response: images_pb2.UpdateImagesResponse = await grpc_client.UpdateImages(
            images_pb2.UpdateImagesRequest(
                image_id=str(images_data[0]["image_id"]),
                update_schema=UpdateImageSchema(name=name_for_update).model_dump_json(
                    exclude_unset=True
                ),
            )
        )

        response_dict: dict = self.proto_to_dict(response)

        files_in_path: list[str] = glob.glob(f"{settings.FILES['images']}/*.*")

        assert files_in_path != files_in_path_before_update

        for image in response_dict["images"]:
            image_from_db = (await get_image_by_uuid_from_database(image["id"]))[0]
            assert os.path.exists(image["file_path"])
            assert image["name"] == name_for_update
            assert image["id"] == str(image_from_db["id"])
            assert image["file_path"] == image_from_db["file_path"]
            assert image["name"] == image_from_db["name"]
