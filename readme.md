# FastAPI-実用的テンプレート(FastAPI Template)

This is a practical template using FastAPI.
It is dockerized including DB (MySQL) and uvicorn.
Package management and task runner are implemented using poetry.
We apologize for the inconvenience.
The following text is in Japanese only.
Please use automatic translation, etc.

FastAPI を使用した実用的なテンプレートです。
DB(MySQL)と uvicorn を含めて docker 化しています。
poetry を使用して、パッケージ管理およびタスクランナーを実装しています。

# 機能追加要望・改善要望・バグ報告(Feature reports, Improvement reports, Bug reports)

Please send improvement requests and bug reports to Issue.
Issue からお願いします。可能な限り対応いたします。

# 必須環境(Required Configuration)

- Python 3.9+

# デモ環境(Heroku Demos)

本リポジトリに、heroku にデプロイするための設定ファイルも含まれています。
デプロイ済の環境は以下から参照できます。

```
https://fastapi-sample-tk.herokuapp.com/docs
```

DB 定義(dbdocs)

```
https://dbdocs.io/marutoraman/fastapi-sample?table=jobs&schema=public&view=table_structure
```

# 機能(Features)

## パッケージ管理、タスクランナー管理(Package management, task runner management)

poetry および poe を使用してパッケージやタスクランナーを管理しています。
詳しい定義内容は、pyproject.toml を参照してください。
[tool.poe.tasks] セクションにタスクランナーを定義しています。

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

そこで、humps を install して、自動的にスネークケースに変換するように
以下のような BaseSchema を作成しています。
この BaseSchema を継承することで、簡単にキャメルケースとスネークケースの相互変換が実現できます。

```python
class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
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

テスト関数の実行毎に DB をクリーンするため、ステートレスなテストが実行できます。
tests/test_data/ 配下でテスト用のデータを定義してください。

## ログの集中管理(Sentry log management)

.env ファイルの SENTRY_SDK_DNS を設定すると、error 以上の logging が発生した場合に
sentry に自動的に logging されます。

## DB マイグレーション(DB migrations)

alembic/versions.py にマイグレーション情報を記述すると、DB マイグレーション(移行)を実施することができます。
以下を実行することで、models の定義と実際の DB との差分から自動的にマイグレーションファイルを作成できます。

```bash
poe makemigrations
```

以下を実行することで、マイグレーションが実行できます。

```bash
poe migrate
```

## fastapi-debug-toolbar

.env ファイルにて DEBUG=true を指定すると、Swaggar 画面から debug-toolbar が起動できます。

SQLAlchemy のクエリや Request など、django-debug-toolbar と同等の内容が確認できます。

## CI/CD

push 時に、Github Actions を使用して、ECS に自動デプロイを行うためのサンプルを記述しています。
以下に AWS の設定情報等をセットします。

※予め、AWS にて ECS 環境を構築しておく必要があります。

.aws/ecs-task-definition.json
.github/workflow/aws.yml

## 自然言語解析(sudachi language analyze)

sudachi アナライザーを使用した日本語言語解析が可能です。
core/language_analyzer.py に実装しています。

## Elasticsearch

実験的に Elasticsearch の docker-compose.yml も定義しています。
FastAPI との連携は未対応のため、別途対応予定です。

# インストール&使い方(Installations & How to use)

### .env ファイルを準備

.env.example を.env にリネームしてください。

### Poetry のインストール

Poetry をローカル PC にインストールします。

実際の動作は docker コンテナ内で行われるので動作上必須ではありませんが、VSCODE で開発する場合のインタープリター設定を行うために必要になります。

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### 依存パッケージのインストール

依存パッケージをローカル PC にインストールします。

```
poetry install
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
poe init-all-tables
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

## poe タブ入力補完設定(Completion)

※docker コンテ内で開発する場合は、Dockerfile に組み込まれているため実行不要です
bash を使用している場合は、以下のコマンドを実行する。
これにより、タスクランナー実行時にタブで入力補完が可能になります。

```bash
 poe _bash_completion >> ~/.bashrc
```

次回 bash 起動時に有効化されるが、即時有効化するためには以下を実行します。

```
. ~/.bashrc
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
