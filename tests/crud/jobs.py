from fastapi.testclient import TestClient

import crud
from tests.utils.test_db_decorator import temp_db
from tests.utils import test_crud
from tests import test_data
from main import app


@temp_db
def test_get_jobs(db):
    test_crud.add_test_data(db, test_data.test_jobs)
    data = crud.job.get_list(db)    
    assert data[0].id
    assert data[0].title
    assert len(data) == 2
    #assert data[0]["deleted_at"]