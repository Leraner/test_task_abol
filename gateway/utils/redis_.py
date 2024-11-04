import json

import settings
from pydantic import BaseModel
from redis.asyncio import Redis


class RedisCache:
    redis = Redis(host=settings.REDIS_HOST, db=settings.REDIS_DB)

    @classmethod
    async def set_cache(cls, key: str, value: BaseModel, expire: int | None = None):
        return await cls.redis.set(
            name=key,
            value=value.model_dump_json(),
            ex=expire if expire else settings.REDIS_EXPIRE_CACHE,
        )

    @classmethod
    async def get_from_cache(cls, key: str) -> None | dict:
        if await cls.redis.exists(key):
            result: bytes = await cls.redis.get(name=key)
            return json.loads(result.decode("utf-8"))
