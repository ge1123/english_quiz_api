# app/exception_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"[{request.method}] {request.url} - HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": exc.status_code},
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()},
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.method} {request.url}: {repr(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )
