from abc import ABC, abstractmethod

from app.schemas.message import OutgoingMessage


class MessagingProvider(ABC):
    @abstractmethod
    async def send_text(self, message: OutgoingMessage) -> dict:
        pass
