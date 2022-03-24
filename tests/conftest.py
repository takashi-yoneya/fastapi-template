from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import create_engine

from core.config import settings
from core.database import SessionLocal
from main import app
from tests.utils.test_crud import clear_and_set_test_data
# from tests.utils.user import authentication_token_from_email
# from tests.utils.utils import get_superuser_token_headers



@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="module")
# def admin_user_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.TEST_USER_EMAIL, db=db
#     )
    
@pytest.fixture(scope="function")
def TestSession():
    '''
    テスト用のＤＢと接続し、テストデータをセットするための処理
    テスト関数実行毎に呼ばれるfixture
    '''
    # settings of test database
    engine = create_engine(f"{settings.TEST_DATABASE_URI}?charset=utf8mb4")

    # テストデータをセット
    clear_and_set_test_data(engine)
    
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run the tests
    yield test_session
    