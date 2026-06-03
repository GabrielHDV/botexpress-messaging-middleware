from fastapi import FastAPI

from app.api.routes.webhook import router as webhook_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Middleware para integrar BotExpress com provedores de mensageria.",
)

app.include_router(webhook_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
    }
