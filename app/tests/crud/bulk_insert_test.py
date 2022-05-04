from tests.test_data import bulk_data_test
from tests.utils import test_crud


def test_bulk_insert(db):
    test_crud.add_test_data(db, bulk_data_test.bulk_data)
