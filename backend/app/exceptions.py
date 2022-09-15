from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

error_message = {'code': 400, 'message': 'Validation error'}


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Response for all Validation errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(error_message),
    )


def not_found():
    """Custom 404 response."""
    return JSONResponse(
        {'code': 404, 'message': 'Item Not Found'}, status_code=404
    )
