from api.endpoints.jobs import *
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from tests import test_data
from tests.utils import test_crud


def test_get_jobs(clear_db, client: TestClient, db: Session):
    test_crud.add_test_data(db, test_data.test_jobs)
    response = client.get("/jobs")
    print(response.request.__dict__)
    print(response.__dict__)
    assert response.status_code == 200
    data = response.json()["data"]
    print(data)
    assert data[0]["id"]
    assert data[0]["title"]
    # assert data[0]["deleted_at"]


def test_create_job(client: TestClient, db: Session):
    test_crud.add_test_data(db, test_data.test_jobs)
    response = client.post("/jobs", json={"title": "creation_job1"})
    print(response.__dict__)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "creation_job1"
    # assert data[0]["deleted_at"]
