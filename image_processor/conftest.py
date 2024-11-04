import asyncio
import datetime
import os
import uuid
import glob
import shutil

import asyncpg
import grpc
import pytest
from jose import jwt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import settings
from protos.images_pb2_grpc import ImageProcessorStub
from tests.utils import KeyAuthClientInterceptorStreamUnary, KeyAuthClientInterceptor

CLEAN_TABLES = [
    "images",
]


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def asyncpg_pool():
    """
    A connection pool allows you to create multiple connections at application startup
    and reuse them for executing requests.
    """
    pool = await asyncpg.create_pool("".join(settings.DATABASE_URL.split("+asyncpg")))
    yield pool
    await pool.close()


@pytest.fixture(scope="session")
async def access_token() -> str:
    payload = {
        "username": "TestUser",
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=1),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@pytest.fixture(scope="function")
def grpc_client(access_token: str):
    channel = grpc.aio.insecure_channel(
        # {settings.HOST}
        f"image_processor:{settings.PORT}",
        interceptors=(
            KeyAuthClientInterceptor(access_token),
            KeyAuthClientInterceptorStreamUnary(access_token),
        ),
    )
    yield ImageProcessorStub(channel)


@pytest.fixture(scope="session")
async def async_session_test():
    async_engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table in CLEAN_TABLES:
                await session.execute(text(f""" TRUNCATE TABLE "{table}" CASCADE;"""))

                if table == "images":
                    for image in glob.glob("media/images/*.*"):
                        os.remove(image)


@pytest.fixture
async def get_image_by_uuid_from_database(asyncpg_pool):
    async def get_image_by_uuid_from_database(image_id: uuid.UUID):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM images WHERE uuid_eq(id, $1);""",
                image_id,
            )

    return get_image_by_uuid_from_database


@pytest.fixture
async def get_all_images_from_database(asyncpg_pool):
    async def get_all_images_from_database():
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM images;""")

    return get_all_images_from_database


@pytest.fixture
async def create_image_in_database(asyncpg_pool):
    async def create_image_in_database(
        image_id: uuid.UUID, name: str, file_path: str, resolution: str, size: int
    ):
        async with asyncpg_pool.acquire() as connection:
            for images_count in range(2):
                shutil.copyfile("tests/resources/image1.png", file_path)

            return await connection.execute(
                """INSERT INTO images (id, name, file_path, upload_date, resolution, size) VALUES ($1, $2, $3, $4, $5, $6)""",
                image_id,
                name,
                file_path,
                datetime.datetime.now(),
                resolution,
                size,
            )

    return create_image_in_database
