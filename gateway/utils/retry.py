import asyncio
from functools import wraps


def retry(times=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == times:
                        raise e
                    await asyncio.sleep(delay)

        return wrapper

    return decorator
