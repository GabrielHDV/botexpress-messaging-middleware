import httpx
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("Erro HTTP tratado: %s", exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Erro de validação: %s", exc.errors())

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Payload inválido",
            "details": exc.errors(),
        },
    )


async def httpx_exception_handler(request: Request, exc: httpx.HTTPError):
    logger.error("Erro em serviço externo: %s", str(exc))

    return JSONResponse(
        status_code=502,
        content={
            "error": "external_service_error",
            "message": "Falha ao comunicar com serviço externo",
        },
    )


async def value_error_handler(request: Request, exc: ValueError):
    logger.error("Erro de configuração: %s", str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "error": "configuration_error",
            "message": str(exc),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Erro inesperado")

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Erro inesperado ao processar a requisição",
        },
    )
