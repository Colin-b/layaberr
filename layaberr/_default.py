from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception(request: Request, exc: HTTPException):
    """
    required:
        - message
    properties:
        message:
            type: string
            description: Description of the error.
            example: This is a description of the error.
    type: object
    """
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


async def exception(request: Request, exc: Exception):
    """
    required:
        - message
    properties:
        message:
            type: string
            description: Description of the error.
            example: This is a description of the error.
    type: object
    """
    return JSONResponse({"message": str(exc)}, status_code=500)
