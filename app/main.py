from fastapi import FastAPI

app = FastAPI(
    title="BotExpress Messaging Middleware",
    version="1.0.0",
    description="Middleware para integrar BotExpress com provedores de mensageria.",
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "API is running",
    }
