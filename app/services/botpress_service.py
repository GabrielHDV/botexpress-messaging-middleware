import asyncio
import logging
from urllib.parse import urljoin

import httpx

from app.core.config import settings
from app.schemas.message import BotResponse, IncomingMessage

logger = logging.getLogger("botexpress-messaging-middleware")

_MAX_RETRIES = 3
_RETRY_BACKOFF = [1, 2, 4] 

class BotpressService:
    async def send_message(self, incoming: IncomingMessage) -> BotResponse:
        if (
            not settings.botexpress_base_url
            or not settings.botexpress_api_key
            or not settings.botexpress_endpoint_path
        ):
            raise ValueError(
                "Configurações do adapter BotExpress não configuradas. "
                "Defina BOTEXPRESS_BASE_URL, BOTEXPRESS_API_KEY e BOTEXPRESS_ENDPOINT_PATH."
            )

        url = self._build_url()
        headers = self._build_headers()
        payload = self._build_payload(incoming)

        last_exc: Exception | None = None

        for attempt, wait in enumerate(_RETRY_BACKOFF, start=1):
            try:
                async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    return BotResponse(text=self._extract_response_text(data))

            except (httpx.HTTPStatusError, httpx.TransportError) as exc:
                last_exc = exc
                logger.warning(
                    "Tentativa %d/%d falhou ao contactar BotExpress: %s",
                    attempt,
                    _MAX_RETRIES,
                    str(exc),
                )

                if attempt < _MAX_RETRIES:
                    await asyncio.sleep(wait)

        logger.error("BotExpress indisponível após %d tentativas", _MAX_RETRIES)
        raise last_exc

    def _build_url(self) -> str:
        base_url = settings.botexpress_base_url.rstrip("/") + "/"
        endpoint_path = settings.botexpress_endpoint_path.lstrip("/")
        return urljoin(base_url, endpoint_path)

    def _build_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        auth_header = settings.botexpress_auth_header
        auth_scheme = settings.botexpress_auth_scheme

        if auth_header.lower() == "authorization":
            headers[auth_header] = f"{auth_scheme} {settings.botexpress_api_key}".strip()
        else:
            headers[auth_header] = settings.botexpress_api_key

        return headers

    def _build_payload(self, incoming: IncomingMessage) -> dict:
        return {
            "user_id": incoming.phone,
            "message": incoming.text,
            "metadata": {
                "provider": incoming.provider,
                "message_id": incoming.message_id,
                "sender_name": incoming.sender_name,
            },
        }

    def _extract_response_text(self, data: dict) -> str:
        text = (
            data.get("text")
            or data.get("message")
            or data.get("response")
            or data.get("output")
            or data.get("answer")
        )

        if not text:
            return "Não consegui processar sua mensagem agora."

        return str(text)
