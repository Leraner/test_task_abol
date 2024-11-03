import fastapi
from api import ImageProcessorRouter
from exceptions import ExceptionHandlers
import uvicorn


app = fastapi.FastAPI()

routers = [
    ImageProcessorRouter,
]


for exception_handler in ExceptionHandlers.exceptions:
    app.add_exception_handler(
        ExceptionHandlers.exceptions[exception_handler],
        getattr(ExceptionHandlers, exception_handler),
    )

for router in routers:
    app.include_router(router.create_router())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
