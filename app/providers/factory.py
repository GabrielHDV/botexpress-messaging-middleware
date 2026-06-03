from app.core.config import settings
from app.providers.base import MessagingProvider
from app.providers.evolution import EvolutionProvider
from app.providers.zapi import ZApiProvider


def get_messaging_provider() -> MessagingProvider:
    provider = settings.messaging_provider.lower()

    if provider == "zapi":
        return ZApiProvider()

    if provider == "evolution":
        return EvolutionProvider()

    raise ValueError(f"Provedor de mensageria não suportado: {settings.messaging_provider}")
