from fastapi.testclient import TestClient

from api.endpoints.jobs import *
from tests.utils.test_db_decorator import temp_db
from tests.utils import test_crud
from tests import test_data
from main import app

client = TestClient(app)

@temp_db
def test_get_jobs(db: Session):
    test_crud.add_test_data(db, test_data.test_jobs)
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()["data"]
    print(data)
    assert data[0]["id"]
    assert data[0]["title"]
    #assert data[0]["deleted_at"]