from fastapi import APIRouter, Body, Depends

from app.core.auth import validate_webhook_secret
from app.core.logger import logger
from app.core.security import mask_phone
from app.providers.base import MessagingProvider
from app.providers.factory import get_messaging_provider
from app.schemas.message import IncomingMessage, OutgoingMessage
from app.services.botexpress_service import BotExpressService
from app.services.idempotency_service import mark_as_processed, was_processed
from app.services.payload_parser import parse_evolution_payload, parse_zapi_payload

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
    dependencies=[Depends(validate_webhook_secret)],
)


async def process_incoming_message(
    incoming: IncomingMessage,
    provider: MessagingProvider,
) -> dict:
    logger.info(
        "Mensagem recebida | provider=%s | phone=%s | message_id=%s",
        incoming.provider,
        mask_phone(incoming.phone),
        incoming.message_id,
    )

    if was_processed(incoming.message_id):
        logger.info(
            "Mensagem duplicada ignorada | provider=%s | message_id=%s",
            incoming.provider,
            incoming.message_id,
        )

        return {
            "status": "ignored",
            "reason": "duplicated_message",
            "provider": incoming.provider,
            "message_id": incoming.message_id,
        }

    bot_response = await BotExpressService().send_message(incoming)

    await provider.send_text(
        OutgoingMessage(
            phone=incoming.phone,
            text=bot_response.text,
            reply_to_message_id=incoming.message_id,
        )
    )

    mark_as_processed(incoming.message_id)

    logger.info(
        "Mensagem processada com sucesso | provider=%s | phone=%s | message_id=%s",
        incoming.provider,
        mask_phone(incoming.phone),
        incoming.message_id,
    )

    return {
        "status": "processed",
        "provider": incoming.provider,
        "message_id": incoming.message_id,
    }


@router.post("/zapi")
async def receive_zapi_message(
    payload: dict = Body(
        ...,
        example={
            "phone": "5535999999999",
            "text": {
                "message": "Olá"
            },
            "messageId": "abc123",
            "senderName": "Gabriel",
        },
    ),
    provider: MessagingProvider = Depends(get_messaging_provider),
):
    incoming = parse_zapi_payload(payload)

    return await process_incoming_message(incoming, provider)


@router.post("/evolution")
async def receive_evolution_message(
    payload: dict = Body(
        ...,
        example={
            "data": {
                "key": {
                    "remoteJid": "5535999999999@s.whatsapp.net",
                    "id": "msg123",
                },
                "message": {
                    "conversation": "Olá"
                },
                "pushName": "Gabriel",
            }
        },
    ),
    provider: MessagingProvider = Depends(get_messaging_provider),
):
    incoming = parse_evolution_payload(payload)

    return await process_incoming_message(incoming, provider)
