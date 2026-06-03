import httpx

from app.core.config import settings
from app.providers.base import MessagingProvider
from app.schemas.message import OutgoingMessage


class EvolutionProvider(MessagingProvider):
    async def send_text(self, message: OutgoingMessage) -> dict:
        if (
            not settings.evolution_base_url
            or not settings.evolution_instance_name
            or not settings.evolution_api_key
        ):
            raise ValueError("Credenciais da Evolution API não configuradas")

        url = (
            f"{settings.evolution_base_url}"
            f"/message/sendText/{settings.evolution_instance_name}"
        )

        headers = {
            "Content-Type": "application/json",
            "apikey": settings.evolution_api_key,
        }

        payload = {
            "number": message.phone,
            "text": message.text,
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
