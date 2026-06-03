import httpx

from app.core.config import settings
from app.schemas.message import BotResponse, IncomingMessage


class BotExpressService:
    async def send_message(self, incoming: IncomingMessage) -> BotResponse:
        if (
            not settings.botexpress_base_url
            or not settings.botexpress_api_key
            or not settings.botexpress_bot_id
        ):
            raise ValueError("Credenciais do BotExpress não configuradas")

        url = f"{settings.botexpress_base_url}/bots/{settings.botexpress_bot_id}/messages"

        headers = {
            "Authorization": f"Bearer {settings.botexpress_api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "user_id": incoming.phone,
            "message": incoming.text,
            "metadata": {
                "provider": incoming.provider,
                "message_id": incoming.message_id,
                "sender_name": incoming.sender_name,
            },
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        text = (
            data.get("text")
            or data.get("message")
            or data.get("response")
            or "Não consegui processar sua mensagem agora."
        )

        return BotResponse(text=text)
