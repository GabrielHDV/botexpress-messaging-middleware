import asyncio
from hashlib import sha256

import httpx

from app.core.config import settings
from app.schemas.message import BotResponse, IncomingMessage


class BotpressService:
    def __init__(self) -> None:
        if not settings.botpress_webhook_id:
            raise ValueError("BOTPRESS_WEBHOOK_ID não configurado")

        self.base_url = f"https://chat.botpress.cloud/{settings.botpress_webhook_id}"

    async def send_message(self, incoming: IncomingMessage) -> BotResponse:
        user_id = self._build_stable_id(f"user:{incoming.provider}:{incoming.phone}")
        conversation_id = self._build_stable_id(
            f"conversation:{incoming.provider}:{incoming.phone}"
        )

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            user_key = await self._create_user(
                client=client,
                user_id=user_id,
                name=incoming.sender_name or incoming.phone,
            )

            await self._get_or_create_conversation(
                client=client,
                user_key=user_key,
                conversation_id=conversation_id,
            )

            await self._send_user_message(
                client=client,
                user_key=user_key,
                conversation_id=conversation_id,
                text=incoming.text,
            )

            bot_text = await self._wait_for_bot_response(
                client=client,
                user_key=user_key,
                conversation_id=conversation_id,
            )

        return BotResponse(text=bot_text)

    async def _create_user(
        self,
        client: httpx.AsyncClient,
        user_id: str,
        name: str,
    ) -> str:
        response = await client.post(
            f"{self.base_url}/users",
            json={
                "id": user_id,
                "name": name,
            },
        )

        response.raise_for_status()
        data = response.json()

        return data["key"]

    async def _get_or_create_conversation(
        self,
        client: httpx.AsyncClient,
        user_key: str,
        conversation_id: str,
    ) -> None:
        response = await client.post(
            f"{self.base_url}/conversations/get-or-create",
            headers={
                "x-user-key": user_key,
                "Content-Type": "application/json",
            },
            json={
                "id": conversation_id,
            },
        )

        response.raise_for_status()

    async def _send_user_message(
        self,
        client: httpx.AsyncClient,
        user_key: str,
        conversation_id: str,
        text: str,
    ) -> None:
        response = await client.post(
            f"{self.base_url}/messages",
            headers={
                "x-user-key": user_key,
                "Content-Type": "application/json",
            },
            json={
                "conversationId": conversation_id,
                "payload": {
                    "type": "text",
                    "text": text,
                },
            },
        )

        response.raise_for_status()

    async def _wait_for_bot_response(
        self,
        client: httpx.AsyncClient,
        user_key: str,
        conversation_id: str,
    ) -> str:
        for _ in range(settings.botpress_polling_attempts):
            await asyncio.sleep(settings.botpress_polling_interval)

            response = await client.get(
                f"{self.base_url}/conversations/{conversation_id}/messages",
                headers={
                    "x-user-key": user_key,
                },
            )

            response.raise_for_status()
            data = response.json()

            messages = data.get("messages", [])

            for message in reversed(messages):
                payload = message.get("payload", {})
                text = payload.get("text")
                user_id = message.get("userId")

                if text and not user_id:
                    return str(text)

        return "Não consegui obter uma resposta do agente no momento."

    def _build_stable_id(self, value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()
