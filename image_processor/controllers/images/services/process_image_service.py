import os
import glob
from io import BytesIO
from typing import Generator, AsyncIterable
from protos import images_pb2
import settings
from PIL import Image, ImageSequence, ImageFile
from schemas import LogicException


class ProcessImageService:

    async def get_image_chunks(
        self, request_iterator: AsyncIterable[images_pb2.UploadImageRequest]
    ) -> tuple[BytesIO, images_pb2.Metadata]:
        buffer = BytesIO()

        metadata: images_pb2.Metadata | None = None

        async for image_chunk in request_iterator:
            if metadata is None:
                if (
                    image_chunk.meta.content_type
                    not in settings.AVAIlABLE_CONTENT_TYPES
                ):
                    # Content-type - не подходит
                    raise LogicException(
                        f"Incorrect file format. Available file formats: {','.join(settings.AVAIlABLE_CONTENT_TYPES)}"
                    )

                metadata = image_chunk.meta

            buffer.write(image_chunk.image)

        if metadata is None:
            raise LogicException("The file has no metadata")

        buffer.seek(0)

        return buffer, metadata

    @staticmethod
    def _process_gif(
        image: ImageFile.ImageFile, target_size: tuple[int, int]
    ) -> Generator[Image.Image, None, None]:
        frames = ImageSequence.Iterator(image)

        for frame in frames:
            resized_frame = frame.resize(target_size, Image.Resampling.LANCZOS)
            grayscale_frame = resized_frame.convert("L")
            yield grayscale_frame

    @staticmethod
    def _process_image(
        image: ImageFile.ImageFile, target_size: tuple[int, int]
    ) -> Image.Image:
        resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
        grayscale_image = resized_image.convert("L")
        return grayscale_image

    def process_image(
        self,
        tmp_image: BytesIO,
        metadata: images_pb2.Metadata,
        target_size: tuple[int, int] = (500, 500),
    ) -> Image.Image | Generator[Image.Image, None, None]:
        image = Image.open(tmp_image, mode="r")

        if metadata.content_type == "image/gif":
            processed_frames = self._process_gif(image, target_size)
            return processed_frames
        else:
            processed_image = self._process_image(image, target_size)
            return processed_image

    @staticmethod
    def save_image(
        file_path: str,
        metadata: images_pb2.Metadata,
        image: Image.Image | Generator[Image.Image, None, None],
    ) -> None:
        image_format = metadata.content_type.split("/")[1]

        if isinstance(image, Generator):
            frame = next(image)
            frame.save(
                file_path,
                format=image_format,
                save_all=True,
                append_images=image,
            )
        else:
            image.save(
                file_path,
                format=image_format,
            )

    @staticmethod
    def rename_images(old_name: str, new_name: str) -> None:
        dir_images = glob.glob(f"{settings.FILES['images']}/*.*")
        for dir_image in dir_images:
            if old_name in dir_image:
                os.rename(dir_image, dir_image.replace(old_name, new_name))

    @staticmethod
    def delete_image(image_path: str) -> None:
        if os.path.exists(image_path):
            os.remove(image_path)
