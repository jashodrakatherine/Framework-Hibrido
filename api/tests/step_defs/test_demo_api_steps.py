"""Step definitions para tests/features/demo_api.feature.

Los steps hablan con `ApiClient` (nunca con `requests` directo), igual que
web habla con Pages/Workflows. El contexto entre steps (la respuesta HTTP)
viaja en un dict simple (fixture `context`). Corre contra
jsonplaceholder.typicode.com, igual que antes.
"""
from pathlib import Path

import pytest
from pytest_bdd import parsers, scenarios, then, when

FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"

scenarios("demo_api.feature", features_base_dir=str(FEATURES_DIR))


@pytest.fixture
def context():
    return {}


@when(parsers.parse("solicito el post con id {post_id:d}"))
def request_post(api_client, context, post_id):
    context["response"] = api_client.get(f"/posts/{post_id}")


@when(parsers.parse('creo un post con título "{title}" y cuerpo "{body}" para el usuario {user_id:d}'))
def create_post(api_client, context, title, body, user_id):
    context["response"] = api_client.post(
        "/posts", json={"title": title, "body": body, "userId": user_id}
    )


@then(parsers.parse("la respuesta debe tener status {status:d}"))
def assert_status(context, status):
    assert context["response"].status_code == status


@then(parsers.parse("el post debe tener id {post_id:d}"))
def assert_post_id(context, post_id):
    assert context["response"].json()["id"] == post_id


@then("el post debe tener título")
def assert_post_has_title(context):
    assert "title" in context["response"].json()


@then(parsers.parse('el post creado debe tener título "{title}"'))
def assert_created_title(context, title):
    assert context["response"].json()["title"] == title


@then("el post creado debe tener id")
def assert_created_id(context):
    assert "id" in context["response"].json()
