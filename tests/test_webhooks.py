from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

AUTH_HEADERS = {
    "X-Webhook-Secret": "dev-secret",
}


def test_zapi_webhook_with_invalid_payload():
    response = client.post("/webhooks/zapi", json={}, headers=AUTH_HEADERS)

    assert response.status_code == 400
    assert response.json() == {
        "error": "http_error",
        "message": "Payload inválido da Z-API: phone e text são obrigatórios",
    }


def test_evolution_webhook_with_invalid_payload():
    response = client.post("/webhooks/evolution", json={}, headers=AUTH_HEADERS)

    assert response.status_code == 400
    assert response.json() == {
        "error": "http_error",
        "message": "Payload inválido da Evolution API: phone e text são obrigatórios",
    }


def test_zapi_webhook_without_secret():
    response = client.post("/webhooks/zapi", json={})

    assert response.status_code == 401
    assert response.json() == {
        "error": "http_error",
        "message": "Webhook secret inválido ou ausente",
    }


def test_zapi_webhook_with_media_payload():
    payload = {
        "phone": "5535999999999",
        "image": {
            "imageUrl": "https://example.com/image.png"
        },
        "messageId": "img123",
        "senderName": "Gabriel",
    }

    response = client.post("/webhooks/zapi", json=payload, headers=AUTH_HEADERS)

    assert response.status_code == 415
    assert response.json() == {
        "error": "http_error",
        "message": (
            "Tipo de mensagem não suportado nesta versão. "
            "O middleware processa apenas mensagens textuais."
        ),
    }


def test_evolution_webhook_with_media_payload():
    payload = {
        "data": {
            "key": {
                "remoteJid": "5535999999999@s.whatsapp.net",
                "id": "img123",
            },
            "message": {
                "imageMessage": {
                    "caption": "imagem de teste"
                }
            },
            "pushName": "Gabriel",
        }
    }

    response = client.post("/webhooks/evolution", json=payload, headers=AUTH_HEADERS)

    assert response.status_code == 415
    assert response.json() == {
        "error": "http_error",
        "message": (
            "Tipo de mensagem não suportado nesta versão. "
            "O middleware processa apenas mensagens textuais."
        ),
    }
