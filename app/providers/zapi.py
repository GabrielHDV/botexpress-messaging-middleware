import httpx

from app.core.config import settings
from app.providers.base import MessagingProvider
from app.schemas.message import OutgoingMessage


class ZApiProvider(MessagingProvider):
    async def send_text(self, message: OutgoingMessage) -> dict:
        if not settings.zapi_instance_id or not settings.zapi_token:
            raise ValueError("Credenciais da Z-API não configuradas")

        url = (
            f"https://api.z-api.io/instances/{settings.zapi_instance_id}"
            f"/token/{settings.zapi_token}/send-text"
        )

        headers = {
            "Content-Type": "application/json",
        }

        if settings.zapi_client_token:
            headers["Client-Token"] = settings.zapi_client_token

        payload = {
            "phone": message.phone,
            "message": message.text,
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
