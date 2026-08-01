"""Prueba de referencia para la capa de API, sobre `core/api_client.py`.

Corre contra jsonplaceholder.typicode.com (API pública gratuita, pensada
para practicar automatización), igual que login.feature usa saucedemo.com
como referencia para la capa web. Sirve de plantilla para nuevas pruebas
de API: siempre a través de `ApiClient`, nunca con `requests` directo.
"""
import pytest


@pytest.mark.smoke
def test_get_post_by_id(api_client):
    response = api_client.get("/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert "title" in body


@pytest.mark.smoke
def test_create_post(api_client):
    payload = {"title": "foo", "body": "bar", "userId": 1}

    response = api_client.post("/posts", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert "id" in body


@pytest.mark.regression
def test_get_nonexistent_post_returns_404(api_client):
    response = api_client.get("/posts/99999")

    assert response.status_code == 404
