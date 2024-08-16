from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


client = TestClient(
    app=app,
    base_url="http://localhost:8000" + settings.API_V1_STR,
)


# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
