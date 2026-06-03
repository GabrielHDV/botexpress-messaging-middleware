from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_zapi_webhook_with_invalid_payload():
    response = client.post("/webhooks/zapi", json={})

    assert response.status_code == 400
    assert response.json() == {
        "error": "http_error",
        "message": "Payload inválido da Z-API: phone e text são obrigatórios",
    }


def test_evolution_webhook_with_invalid_payload():
    response = client.post("/webhooks/evolution", json={})

    assert response.status_code == 400
    assert response.json() == {
        "error": "http_error",
        "message": "Payload inválido da Evolution API: phone e text são obrigatórios",
    }
