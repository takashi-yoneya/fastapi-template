from core.database import get_db
from main import app
from sqlalchemy import create_engine


def temp_db(f):
    """
    pytestでテスト用のＤＢを使用する場合のデコレーター
    エンドポイントのテストで使用する
    """

    def func(TestSession, *args, **kwargs):
        # テスト用のDBに接続するためのSessionLocalをfixtureから受け取る

        def override_get_db():
            try:
                db = TestSession()
                yield db
            finally:
                db.close()

        # fixtureから受け取るSessionLocalを使うようにget_dbを強制的に変更
        # これによりAPIコール時のget_dbがテスト用に指定したものに自動的に置き換わる
        app.dependency_overrides[get_db] = override_get_db

        # テスト関数の引数にdbが含まれる場合は、テスト用のdbセッションをセットする
        if "db" in f.__code__.co_varnames:
            print(args, kwargs)
            db = TestSession()
            f(db=db, *args, **kwargs)
        else:
            f(*args, **kwargs)

        # get_dbを元に戻す
        app.dependency_overrides[get_db] = get_db

    return func
