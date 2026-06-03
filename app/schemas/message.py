from pydantic import BaseModel, Field


class IncomingMessage(BaseModel):
    provider: str = Field(..., examples=["zapi", "evolution"])
    phone: str
    text: str
    message_id: str | None = None
    sender_name: str | None = None


class OutgoingMessage(BaseModel):
    phone: str
    text: str
    reply_to_message_id: str | None = None


class BotResponse(BaseModel):
    text: str
