from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    app_name: str = "BotExpress Messaging Middleware"

    webhook_secret: str | None = None

    messaging_provider: str = "zapi"

    zapi_instance_id: str | None = None
    zapi_token: str | None = None
    zapi_client_token: str | None = None

    evolution_base_url: str | None = None
    evolution_instance_name: str | None = None
    evolution_api_key: str | None = None

    botexpress_base_url: str | None = None
    botexpress_api_key: str | None = None
    botexpress_endpoint_path: str | None = None
    botexpress_auth_header: str = "Authorization"
    botexpress_auth_scheme: str = "Bearer"

    request_timeout: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
