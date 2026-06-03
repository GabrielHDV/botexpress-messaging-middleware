from fastapi import HTTPException

from app.schemas.message import IncomingMessage


def parse_zapi_payload(payload: dict) -> IncomingMessage:
    phone = payload.get("phone")
    message_id = payload.get("messageId")
    sender_name = payload.get("senderName")

    text_content = payload.get("text")

    if isinstance(text_content, dict):
        text = text_content.get("message")
    else:
        text = text_content

    if not phone or not text:
        raise HTTPException(
            status_code=400,
            detail="Payload inválido da Z-API: phone e text são obrigatórios",
        )

    return IncomingMessage(
        provider="zapi",
        phone=phone,
        text=text,
        message_id=message_id,
        sender_name=sender_name,
    )


def parse_evolution_payload(payload: dict) -> IncomingMessage:
    data = payload.get("data", {})

    key = data.get("key", {})
    message = data.get("message", {})

    raw_phone = key.get("remoteJid", "")
    phone = raw_phone.replace("@s.whatsapp.net", "")

    message_id = key.get("id")

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text")
    )

    sender_name = data.get("pushName")

    if not phone or not text:
        raise HTTPException(
            status_code=400,
            detail="Payload inválido da Evolution API: phone e text são obrigatórios",
        )

    return IncomingMessage(
        provider="evolution",
        phone=phone,
        text=text,
        message_id=message_id,
        sender_name=sender_name,
    )
