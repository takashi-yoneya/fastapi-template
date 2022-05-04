import crud
from fastapi.testclient import TestClient
from main import app
from tests import test_data
from tests.utils import test_crud


def test_get_jobs(db):
    test_crud.add_test_data(db, test_data.test_jobs)
    data = crud.job.get_list(db)
    assert data[0].id
    assert data[0].title
    assert len(data) == 2
    # assert data[0]["deleted_at"]
