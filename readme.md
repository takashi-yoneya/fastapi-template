FastAPI-実用的テンプレート
====
FastAPIを使用した実用的なテンプレートです。
DB(MySQL)とuvicornを含めてdocker化しています。
poetryを使用して、パッケージ管理およびタスクランナーを実装しています。

# デモ環境(heroku)
本リポジトリに、herokuにデプロイするための設定ファイルも含まれております。<br>
デプロイ済の環境は以下から参照できます。
```
https://fastapi-sample-tk.herokuapp.com/docs
```

# 機能(Features)

## DBレコードの作成・取得・更新・削除(CRUD)
crud/base.py にCRUDの共通Classを記述しています。
それ以外のcrud配下のファイルで、CRUD処理をoverrideすることができます。

## 権限(scopes)
特定のUserのみが実行できるAPIを作成する場合は、
tableの user.scopes の値とrouterに指定したscopeを一致させる。

```
@router.get(
    "/{id}",
    response_model=schemas.UserResponse,
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
```

## キャメルケースとスネークケースの相互変換
Pythonではスネークケースが標準ですが、Javascriptではキャメルケースが標準なため、単純にpydanticでschemaを作成しただけでは
jsonレスポンスにスネークケースを使用せざるをえない問題があります。

そこで、humpsをinstallして、自動的にスネークケースに変換するように
以下のようなBaseSchemaを作成しています。
このBaseSchemaを継承することで、簡単にキャメルケースとスネークケースの相互変換が実現できます。

```
class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel 
        allow_population_by_field_name = True
```

## バッチ処理(batch)
サブディレクトリ配下のpyファイルから、別ディレクトリのファイルをimportする場合は
その前に以下のコードを記述する必要がある。

```
sys.path.append(str(Path(__file__).absolute().parent.parent))
```

batch/__set_base_path__.py に記述し、各ファイルの先頭でimportすることで
より簡単にimportできるようにしています。


## Settings
BaseSettingsを継承して共通設定Classを作成している。
.envファイルから自動的に設定を読み込む他、個別に設定を定義することもできる。

## ErrorException
exceptions/error_messages.py にエラーメッセージを定義している。
APIExceptionと併せて以下のように、呼び出すことで、エラーレスポンスを作成できる。
```
raise APIException(ErrorMessage.ID_NOT_FOUND)
```

## logging
logger_config.yaml から設定を読み込む。

## テスト
tests/ 配下に、テスト関連の処理を、まとめている。

テスト関数の実行毎にDBをクリーンするため、ステートレスなテストが実行できます。
tests/test_data/ 配下にテスト用データをセットする。

## ログの集中管理
.envファイルにsentryのDNSを設定すると、error以上のloggingが発生した場合に
sentryに自動的にloggingされます。

## DBマイグレーション
alembic/versions.py にマイグレーション情報を記述すると、DBマイグレーション(移行)を実施することができます。


## パッケージ管理
poetryを使用して、パッケージ管理を実施。
また、poethepoetを使用するすることでタスクランナー機能を追加している。


## CI/CD
push時に、Github Actionsを使用して、ECSに自動デプロイを行います。
以下にAWSの設定情報等をセットします。
.aws/ecs-task-definition.json
.github/workflow/aws.yml

# インストール&使い方(Installations & How to use)
## Poetryのインストール
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

## 依存パッケージのインストール
```
poetry install
```

## dockerコンテナのビルド & 起動
```
docker-compose up --build
```

## API管理画面(OpenAPI)表示
ローカル環境
```
http://localhost:8090/docs
```
