import pytest

from app.core.database import client


@pytest.fixture(name="client")
def client_fixture():
    yield client


def test_ping(client):
    database = client["you-only-search-once"]
    collection_list = database.list_collection_names()
    for c in collection_list:
        assert c == "dev"
