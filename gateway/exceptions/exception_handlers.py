from grpc.aio import AioRpcError

# from grpc import StatusCode
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class ExceptionHandlers:
    exceptions = {"grpc_error_handler": AioRpcError}

    @classmethod
    async def grpc_error_handler(cls, _: Request, exc: AioRpcError):
        # Need to send exceptions from status
        return JSONResponse(status_code=400, content={"detail": exc.details()})
