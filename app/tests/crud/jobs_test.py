import crud
from crud import job
from tests import test_data

from ..utils import test_crud


def test_get_jobs(db):
    test_crud.add_test_data(db, test_data.test_jobs())
    job.get_list(db)
    data = crud.job.get_list(db)
    print(data)
    assert data[0].id
    assert data[0].title
    assert len(data) == 2
    # assert data[0]["deleted_at"]
