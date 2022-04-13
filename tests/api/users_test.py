from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.endpoints.jobs import *
from main import app
from tests import test_data
from tests.utils import test_crud
from core.config import settings



def test_get_users_me(client: TestClient, db: Session, auth_headers):
    # print(auth_headers)
    respose = client.get("users/me", headers=auth_headers)
    data = respose.json()
    print(data)

    assert data["email"] == settings.TEST_USER_EMAIL