from fastapi import Header, HTTPException

from app.core.config import settings


async def validate_webhook_secret(
    x_webhook_secret: str | None = Header(default=None),
) -> None:
    if not settings.webhook_secret:
        return

    if x_webhook_secret != settings.webhook_secret:
        raise HTTPException(
            status_code=401,
            detail="Webhook secret inválido ou ausente",
        )
