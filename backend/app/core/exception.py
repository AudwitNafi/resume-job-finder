from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.schemas.exception_dto import ValidationErrorResponse
from fastapi import Request
from app.core.logger import logger


# Custom validation error handler for FastAPI to standardize validation responses
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Formats FastAPI validation errors into a unified JSON structure.
    """
    errors = exc.errors()
    custom_errors = [
        {
            "field": error["loc"][-1],
            "message": error["msg"],
        }
        for error in errors
    ]
    logger.exception(f"Validation failed for request {request.url}: {custom_errors}")
    error_response = ValidationErrorResponse(
        message="Payload Validation failed", errors=custom_errors, success=False
    )
    return JSONResponse(status_code=422, content=error_response.model_dump())


async def value_error_handler(request: Request, exc: ValueError):
    logger.exception(f"ValueError on request {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "message": "Invalid value",
            "errors": [{"field": None, "message": str(exc)}],
            "success": False,
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on request {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "errors": [{"field": None, "message": str(exc)}],
            "success": False,
        },
    )
