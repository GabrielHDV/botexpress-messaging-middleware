from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    app_name: str = "Botpress Messaging Middleware"

    webhook_secret: str | None = None

    messaging_provider: str = "zapi"

    zapi_instance_id: str | None = None
    zapi_token: str | None = None
    zapi_client_token: str | None = None

    evolution_base_url: str | None = None
    evolution_instance_name: str | None = None
    evolution_api_key: str | None = None

    botpress_webhook_id: str | None = None
    botpress_polling_attempts: int = 8
    botpress_polling_interval: float = 1.0

    request_timeout: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
