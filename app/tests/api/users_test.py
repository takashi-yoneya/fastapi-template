from api.endpoints.jobs import *
from core.config import settings
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from tests import test_data
from tests.utils import test_crud


def test_get_users_me(client: TestClient, db: Session, auth_headers):
    # print(auth_headers)
    respose = client.get("users/me", headers=auth_headers)
    data = respose.json()
    print(data)

    assert data["email"] == settings.TEST_USER_EMAIL
