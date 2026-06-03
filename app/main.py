import httpx
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api.routes.webhook import router as webhook_router
from app.core.config import settings
from app.exceptions.handlers import (
    generic_exception_handler,
    http_exception_handler,
    httpx_exception_handler,
    validation_exception_handler,
    value_error_handler,
)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Middleware para integrar BotExpress com provedores de mensageria.",
)

app.include_router(webhook_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(httpx.HTTPError, httpx_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
    }
