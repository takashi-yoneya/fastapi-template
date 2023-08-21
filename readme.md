# FastAPI-実用的テンプレート(FastAPI Template)

This is a practical template using FastAPI.
It is dockerized including DB (MySQL) and uvicorn.
Package management is implemented using rye.
We apologize for the inconvenience.
The following text is in Japanese only.
Please use automatic translation, etc.

FastAPI を使用した実用的なテンプレートです。
DB(MySQL)と uvicorn を含めて docker 化しています。
rye を使用して、パッケージ管理を実装しています。

# 機能追加要望・改善要望・バグ報告(Feature reports, Improvement reports, Bug reports)

Please send improvement requests and bug reports to Issue.
Issue からお願いします。可能な限り対応いたします。

# 必須環境(Required Configuration)

- Python 3.9+

# SQLAlchemy1.4(sync)版　（旧バージョン）
SQLAlchemy1.4(sync)版は旧バージョンのため、今後Updateの予定はありませんが、使用したい場合はmaster-old-sqlalchemy14 ブランチを参照してください。

# デモ環境(Heroku Demos)

本リポジトリに、heroku にデプロイするための設定ファイルも含まれています。
デプロイ済の環境は以下から参照できます。

```
https://fastapi-sample-tk.herokuapp.com/docs
```

# プロジェクト構造(Project Structures)

```text
.
├── Dockerfile          // 通常使用するDockerfile
├── Dockerfile.lambda   // Lambdaにデプロイする場合のDockerfile
├── LICENSE.md
├── Makefile            // タスクランナーを定義したMakefile
├── Procfile
├── alembic             // migrationに使用するalembicのディレクトリ
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 20230131-0237_.py
├── alembic.ini
├── app                 // mainのソースコードディレクト遺r
│   ├── __init__.py
│   ├── api             // WebAPI Endpoint
│   │   └── endpoints
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── develop.py
│   │       ├── tasks.py
│   │       ├── todos.py
│   │       └── users.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── __set_base_path__.py
│   │   └── user_creation.py
│   ├── core            // 共通で共通するCore機能
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logger
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   └── utils.py
│   ├── crud            // crudディレクトリ（Sqlalchemy v1.4のため、メンテ停止）
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── tag.py
│   │   ├── todo.py
│   │   └── user.py
│   ├── crud_v2　       // crudディレクトリ (sqlalchemy v2対応)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── tag.py
│   │   ├── todo.py
│   │   └── user.py
│   ├── exceptions      // expectionsの定義
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── error_messages.py
│   │   └── exception_handlers.py
│   ├── logger_config.yaml
│   ├── main.py         // fastapiのmainファイル。uvicornで指定する
│   ├── models          // DBテーブルのmodel
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── tags.py
│   │   ├── todos.py
│   │   ├── todos_tags.py
│   │   └── users.py
│   └── schemas         // 外部入出力用のschema
│       ├── __init__.py
│       ├── core.py
│       ├── language_analyzer.py
│       ├── request_info.py
│       ├── tag.py
│       ├── todo.py
│       ├── token.py
│       └── user.py
├── docker-compose.ecs.yml
├── docker-compose.es.yml
├── docker-compose.yml
├── docs
│   ├── docs
│   │   ├── index.md
│   │   └── install.md
│   └── mkdocs.yml
├── elasticsearch
│   ├── docker-compose.yml
│   ├── elasticsearch
│   │   └── Dockerfile.es
│   ├── logstash
│   │   ├── Dockerfile
│   │   └── pipeline
│   │       └── main.conf
│   └── readme.md
├── flake8.ini
├── frontend_sample             // Frontend(react)からBackendを呼び出すサンプル
│   ├── README.md
│   ├── next.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   └── vercel.svg
│   ├── src
│   │   ├── api_clients
│   │   │   ├── api.ts
│   │   │   ├── base.ts
│   │   │   ├── client.ts
│   │   │   ├── common.ts
│   │   │   ├── configuration.ts
│   │   │   ├── git_push.sh
│   │   │   └── index.ts
│   │   ├── components
│   │   │   └── templates
│   │   │       └── todos
│   │   │           ├── TodoCreateTemplate
│   │   │           │   └── TodoCreateTemplate.tsx
│   │   │           ├── TodoUpdateTemplate
│   │   │           │   └── TodoUpdateTemplate.tsx
│   │   │           └── TodosListTemplate
│   │   │               └── TodosListTemplate.tsx
│   │   ├── config.ts
│   │   ├── lib
│   │   │   └── hooks
│   │   │       └── api
│   │   │           ├── index.ts
│   │   │           └── todos.ts
│   │   ├── pages
│   │   │   ├── _app.tsx
│   │   │   ├── index.tsx
│   │   │   └── todos
│   │   │       ├── create.tsx
│   │   │       ├── edit.tsx
│   │   │       └── list.tsx
│   │   ├── styles
│   │   │   ├── Home.module.css
│   │   │   └── globals.css
│   │   └── types
│   │       └── api
│   │           └── index.ts
│   └── tsconfig.json
├── mypy.ini
├── pyproject.toml
├── Makefile
├── readme.md
├── requirements-dev.lock
├── requirements.lock
├── runtime.txt
├── seeder                        // seedの定義、インポーター
│   ├── run.py
│   └── seeds_json
│       ├── todos.json
│       └── users.json
└── tests                         // test
    ├── __init__.py
    ├── base.py
    ├── conftest.py
    ├── testing_utils.py
    └── todos
        ├── __init__.py
        ├── conftest.py
        └── test_todos.py
```

# 機能(Features)

## パッケージ管理、タスクランナー管理(Package management, task runner management)

rye を使用してパッケージ管理を行い、makefileでタスクランナーを管理しています。
詳しい定義内容は、Makefile を参照してください。

## DB レコードの作成・取得・更新・削除(CRUD)

crud/base.py に CRUD の共通 Class を実装しています。
個別の CRUD 実装時は、この共通 Class を継承して個別処理を実装してください。

## 論理削除の CRUD 管理(Software delete)

DB レコード削除時に実際には削除せず deleted_at に削除日付をセットすることで
論理削除を実装しています。

以下のように SQLAlchemy の event 機能を使用して、ORM 実行後に自動的に論理削除レコードを除外するための filter を追加しています。
これにより、個別の CRUD で論理削除を実装する必要がなくなります。
include_deleted=True とすると、論理削除済レコードも取得できます。

```python
@event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state):
    """
    論理削除用のfilterを自動的に適用する
    以下のようにすると、論理削除済のデータも含めて取得可能
    query(...).filter(...).execution_options(include_deleted=True)
    """
    logger.info(execute_state)
    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                ModelBase,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

```

## 権限(Scopes)

特定の User のみが実行できる API を作成する場合は、
table の user.scopes の値と router に指定した scope を一致させてください。

```python
@router.get(
    "/{id}",
    response_model=schemas.UserResponse,
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
```

## キャメルケースとスネークケースの相互変換(Mutual conversion between CamelCase and SnakeCase)

Python ではスネークケースが標準ですが、Javascript ではキャメルケースが標準なため
単純に pydantic で schema を作成しただけでは、json レスポンスにスネークケースを使用せざるをえない問題があります。

そこで、以下のような BaseSchema を作成して、キャメルケース、スネークケースの相互変換を行なっています。
pydantic v2では、```from pydantic.alias_generators import to_camel```をインポートして、ConfigDictのalias_generatorにセットすることで、簡単にキャメルケースとスネークケースの相互変換が実現できます。

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseSchema(BaseModel):
    """全体共通の情報をセットするBaseSchema"""

    # class Configで指定した場合に引数チェックがされないため、ConfigDictを推奨
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, strict=True)


```

## OpenAPI Generator を使用してバックエンドの型定義をフロントエンドでも使用する

FastAPI を使用するとエンドポイントを作成した段階で openapi.json が自動生成されます。

OpenAPI-Generator は、この openapi.json を読み込んで、フロントエンド用の型定義や API 呼び出し用コードを自動生成する仕組みです。

docker-compose 内で定義しており、docker compose up で実行される他、`make openapi-generator`を実行すると openapi-generator だけを実行できます。

生成されたコードは、`/fontend_sample/src/api_clients`に格納されます。(-o オプションで変更可能)

```yml
# openapiのclient用のコードを自動生成するコンテナ
openapi-generator:
  image: openapitools/openapi-generator-cli
  depends_on:
    web:
      condition: service_healthy
  volumes:
    - ./frontend_sample:/fontend_sample
  command: generate -i http://web/openapi.json -g typescript-axios -o /fontend_sample/src/api_clients --skip-validate-spec
  networks:
    - fastapi_network
```

## バッチ処理(Batch)

サブディレクトリ配下の py ファイルから、別ディレクトリのファイルを import する場合は
その前に以下のコードを記述する必要があります。

```python
sys.path.append(str(Path(__file__).absolute().parent.parent))
```

batch/**set_base_path**.py に記述し、各ファイルの先頭で import することで
より簡単に import できるようにしています。

## Settings

core/config.py にて、BaseSettings を継承して共通設定 Class を定義しています。
.env ファイルから自動的に設定を読み込むことができる他、個別に設定を定義することもできます。

## CORS-ORIGIN

CORS ORIGIN は大きく２パターンの設定方法があります。
allow_origins に list を指定する方法では、settings.CORS_ORIGINS に url を指定することで
任意の ORIGIN が設定可能です。
また、https://\*\*\*\*.example.com のようにサブドメインを一括で許可したい場合は
allow_origin_regex に以下のように正規表現で URL パターンを指定してください。

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_origin_regex=r"^https?:\/\/([\w\-\_]{1,}\.|)example\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## ErrorException

exceptions/error_messages.py にエラーメッセージを定義しています。
APIException と併せて以下のように、呼び出すことで、任意の HTTP コードのエラーレスポンスを作成できます。

```python
raise APIException(ErrorMessage.INTERNAL_SERVER_ERROR)
```

レスポンス例

```
http status code=400
{
  "detail": {
    "error_code": "INTERNAL_SERVER_ERROR",
    "error_msg": "システムエラーが発生しました、管理者に問い合わせてください"
  }
}
```

## AppManager

FastAPIのmount機能を使うと、多くのAPIを作成する場合などopenapiを複数画面に分割することができますが、openapi間のリンクが不便になる問題があります。
そこで、複数のFastAPIのappを統合管理できるFastAPIAppManagerクラスを構築しています。

FastAPIAppManagerを使用して、複数のappをadd_appで追加していくことで、複数のappに対する共通処理を実行することができます。

一例として以下の実装では、setup_apps_docs_link()でopenapiの上部に表示するapp間のlinkを生成しています。

```python
# main.py
app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    debug=settings.DEBUG or False,
)
app_manager = FastAPIAppManager(root_app=app)
# appを分割する場合は、add_appで別のappを追加する
app_manager.add_app(path="admin", app=admin_app.app)
app_manager.add_app(path="other", app=other_app.app)
app_manager.setup_apps_docs_link()
```

```python
# app_manager.py
class FastAPIAppManager():

    def __init__(self, root_app: FastAPI):
        self.app_path_list: list[str] = [""]
        self.root_app: FastAPI = root_app
        self.apps: list[FastAPI] = [root_app]

    def add_app(self, app: FastAPI, path: str) -> None:
        self.apps.append(app)
        if not path.startswith("/"):
            path = f"/{path}"
        else:
            path =path
        self.app_path_list.append(path)
        app.title = f"{self.root_app.title}({path})"
        app.version = self.root_app.version
        app.debug = self.root_app.debug
        self.root_app.mount(path=path, app=app)

    def setup_apps_docs_link(self) -> None:
        """ 他のAppへのリンクがopenapiに表示されるようにセットする """
        for app, path in zip(self.apps, self.app_path_list):
            app.description = self._make_app_docs_link_html(path)

    def _make_app_docs_link_html(self, current_path: str) -> str:
        # openapiの上部に表示する各Appへのリンクを生成する
        descriptions = [
            f"<a href='{path}/docs'>{path}/docs</a>" if path != current_path else f"{path}/docs"
            for path in self.app_path_list
        ]
        descriptions.insert(0, "Apps link")
        return "<br>".join(descriptions)
```


## logging

logger_config.yaml で logging 設定を管理しています。可読性が高くなるように yaml で記述しています。
uviron の起動時に`--log-config ./app/logger_config.yaml` のように option 指定して logger 設定を行います。

```yaml
version: 1
disable_existing_loggers: false # 既存のlogger設定を無効化しない

formatters: # formatterの指定、ここではjsonFormatterを使用して、json化したlogを出力するようにしている
  json:
    format: "%(asctime)s %(name)s %(levelname)s  %(message)s %(filename)s %(module)s %(funcName)s %(lineno)d"
    class: pythonjsonlogger.jsonlogger.JsonFormatter

handlers: # handerで指定した複数種類のログを出力可能
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: json
    stream: ext://sys.stdout

loggers: # loggerの名称毎に異なるhandlerやloglevelを指定できる
  backend:
    level: INFO
    handlers: [console]
    propagate: false

  gunicorn.error:
    level: DEBUG
    handlers: [console]
    propagate: false

  uvicorn.access:
    level: INFO
    handlers: [console]
    propagate: false

  sqlalchemy.engine:
    level: INFO
    handlers: [console]
    propagate: false

  alembic.runtime.migration:
    level: INFO
    handlers: [console]
    propagate: false

root:
  level: INFO
  handlers: [console]
```

## テスト(Testing)

tests/ 配下に、テスト関連の処理を、まとめています。

実行時は、`make test`で実行できます。個々のテストケースを実行する場合は`make docker-run`でコンテナに入った後に`pytest tests/any/test/path.py`のようにファイルやディレクトリを指定して実行できます。

pytest.fixture を使用して、テスト関数毎に DB の初期化処理を実施しているため、毎回クリーンな DB を使用してステートレスなテストが可能です。

DB サーバーは docker で起動する DB コンテナを共用しますが、同じデータベースを使用してしまうと、テスト時にデータがクリアされてしまうので、別名のデータベースを作成しています。

pytest では conftest.py に記述した内容は自動的に読み込まれるため、conftest.py にテストの前処理を記述しています。

tests/conftest.py には、テスト全体で使用する設定の定義や DB や HTTP クライアントの定義を行っていおます。

conftest.py は実行するテストファイルのある階層とそれより上の階層にあるものしか実行されないため、以下の例で test_todos.py を実行した場合は、`tests/todos/conftest.py` と `tests/conftest.py` のみが実行されます。

```
test/
  conftest.py
  -- todos/
   -- conftest.py
   -- test_todos.py
  -- any-test/
   -- conftest.py
   -- test_any-test.py
```

この仕様を活かして、todos/などの個々のテストケースのディレクトリ配下の conftest.py では、以下のように対象のテストケースのみで使用するデータのインポートを定義しています。

```python
@pytest.fixture
def data_set(db: Session):
    insert_todos(db)


def insert_todos(db: Session):
    now = datetime.datetime.now()
    data = [
        models.Todo(
            id=str(i),
            title=f"test-title-{i}",
            description=f"test-description-{i}",
            created_at=now - datetime.timedelta(days=i),
        )
        for i in range(1, 25)
    ]
    db.add_all(data)
    db.commit()
```

fixture で定義した data_set は、以下のようにテスト関数の引数に指定することで、テスト関数の前提処理として実行することができます。

引数に、`authed_client: Client`を指定することで、ログイン認証済の HTTP クライアントが取得できます。`client: Client`を指定した場合は、未認証の HTTP クライアントが取得できます。

API エンドポイント経由のテストではなく、db セッションを直接指定するテストの場合は、`db: Session`を引数に指定することで、テスト用の db セッションを取得できます。

```python
    def test_get_by_id(
        self,
        authed_client: Client,
        id: str,
        expected_status: int,
        expected_data: Optional[dict],
        expected_error: Optional[dict],
        data_set: None, # <-- here
    ) -> None:
        self.assert_get_by_id(
            client=authed_client,
            id=id,
            expected_status=expected_status,
            expected_data=expected_data,
        )
```

```tests/base.py```にAPIテスト用のベースClassが定義されているので、これを継承することで、簡単にテスト関数を構築することができます。

以下の例では、TestBaseクラスを継承して、TestTodosクラスを作成しています。ENDPOINT_URIにテスト対象のAPIエンドポイントのURIを指定することで、CRUD全体で使用できます。

pytestのparametrizeを使用しており、１つのテスト関数で複数のテストケースを定義できます。



```python
class TestTodos(TestBase):
    ENDPOINT_URI = "/todos"

    """create
    """

    @pytest.mark.parametrize(
        ["data_in", "expected_status", "expected_data", "expected_error"],
        [
            pytest.param(
                TodoCreate(title="test-create-title", description="test-create-description").model_dump(by_alias=True),
                status.HTTP_200_OK,
                {"title": "test-create-title", "description": "test-create-description"},
                None,
                id="success",
            ),
            pytest.param(
                TodoCreate(title="test-create-title", description="test-create-description").model_dump(by_alias=True),
                status.HTTP_200_OK,
                {"title": "test-create-title", "description": "test-create-description"},
                None,
                id="any-test-case",
            )
        ],
    )
    def test_create(
        self,
        authed_client: Client,
        data_in: dict,
        expected_status: int,
        expected_data: Optional[dict],
        expected_error: Optional[dict],
    ) -> None:
        self.assert_create(
            client=authed_client,
            data_in=data_in,
            expected_status=expected_status,
            expected_data=expected_data,
        )
```

## ログの集中管理(Sentry log management)

.env ファイルの SENTRY_SDK_DNS を設定すると、error 以上の logging が発生した場合に
sentry に自動的に logging されます。

## DB マイグレーション(DB migrations)

alembic/versions.py にマイグレーション情報を記述すると、DB マイグレーション(移行)を実施することができます。
以下を実行することで、models の定義と実際の DB との差分から自動的にマイグレーションファイルを作成できます。

```bash
make makemigrations m="any-migration-description-message"
```

以下を実行することで、マイグレーションが実行できます。

```bash
make migrate
```

## fastapi-debug-toolbar

.env ファイルにて DEBUG=true を指定すると、Swaggar 画面から debug-toolbar が起動できます。

SQLAlchemy のクエリや Request など、django-debug-toolbar と同等の内容が確認できます。

## Linter
ruffというrustで構築された高速なLinterを使用しています。
pre-commitで実行することを想定しています。

## CI/CD

push 時に、Github Actions を使用して、ECS に自動デプロイを行うためのサンプルを記述しています。
以下に AWS の設定情報等をセットします。

※予め、AWS にて ECS 環境を構築しておく必要があります。

.aws/ecs-task-definition.json
.github/workflow/aws.yml

## Elasticsearch

実験的に Elasticsearch の docker-compose.yml も定義しています。
FastAPI との連携は未対応のため、別途対応予定です。

# インストール&使い方(Installations & How to use)

### .env ファイルを準備

.env.example を.env にリネームしてください。

### Rye のインストール

以下のコマンドで、Rye をローカル PC にインストールします。

```bash
curl -sSf https://rye-up.com/get | bash
```


### 依存パッケージのインストール

依存パッケージをローカル PC にインストールします。
Appの実際の動作はDockerコンテナ内で行われますが、VSCODEのインタープリター設定で使用するために、ローカルPCにもパッケージをインストールします。

```
rye sync
```

### docker コンテナのビルド & 起動

```
docker compose up --build
```

### Web コンテナ内に入る

以下のいずれかのコマンドで Web コンテナ内に入ることができます。

```bash
docker compose run --rm web bash
```

or

Linux or macOS only

```bash
make docker-run
```

### DB 初期化、migration、seed 投入

コンテナ内で以下を実行することで、DB の初期化、migrate、seed データ投入までの一連の処理を一括で行うことができます。

```bash
make init-db
```

## API 管理画面(OpenAPI)表示

ローカル環境

```
http://localhost:8888/docs
```

Debug モード(F5 押下)で起動した場合
※Debug モードの場合は、ブレークポイントでローカル変数を確認できます。

```
http://localhost:8889/docs
```

## pre-commit
commit前にlinter等のチェックを自動で行う場合は,pre-commitをインストール後に、以下コマンドでpre-commitを有効化することで、commit時に自動的にチェックができるようになります。

```bash
pre-commit install
```

## フロントエンドサンプル(Next.js)

フロントエンドから API を呼び出すサンプルを`/fontend_sample`に記述しています。

以下のコマンドで module をインストールできます。

```bash
cd /fontend_sample
npm ci
```

以下のコマンドで、Next サーバーを立ち上げることができます。

```bash
npm run dev
```

```
http://localhost:3000
```

# デプロイ(Deploy to heroku)

heroku-cli を使用した heroku へのデプロイ方法を紹介します。
github からの自動デプロイは heroku 側のセキュリティ問題により停止されているので、手動で heroku に push します。

## heroku-cli のインストール

以下を参考にインストール

https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

## app の作成

APPNAME は任意の名称を指定（全ユーザーでユニークである必要があります）

```
heroku create APPNAME
```

## git に heroku のリモートリポジトリをセット

```
heroku git:remote --app APPNAME
```

## push

```
git push heroku master
```

## heroku-cli に heroku-config をインストール

本リポジトリでは、.env ファイル経由で設定を読み込んでいるため
heroku でも.env ファイルを有効にする必要があります。

```bash
heroku plugins:install heroku-config
```

## .env ファイルを push

```bash
heroku config:push
```

## heroku 再起動

```bash
heroku restart
```

# ライセンス(License)

https://choosealicense.com/licenses/mit/
