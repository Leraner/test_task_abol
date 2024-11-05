import fastapi
from api import ImageProcessorRouter, AuthRouter
from exceptions import ExceptionHandlers
import uvicorn
import settings


app = fastapi.FastAPI()

routers = [
    ImageProcessorRouter,
    AuthRouter,
]


for exception_handler in ExceptionHandlers.exceptions:
    app.add_exception_handler(
        ExceptionHandlers.exceptions[exception_handler],
        getattr(ExceptionHandlers, exception_handler),
    )

for router in routers:
    app.include_router(router.create_router())

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.GATEWAY_HOST, port=settings.GATEWAY_PORT, reload=True
    )
