FastAPI-実用的テンプレート
====
作成中...

# Demo
## ECS Fargateにデプロイ済のデモURL
http://fastapi-sample-backend-alb-1201223431.us-west-1.elb.amazonaws.com/docs

# Features
- fastapi: バックエンドフレームワーク
- crud(sqlalchemy): CRUD
- testing: テスト
- logging: ログ出力
- error handling: エラー管理
- auth scope: 権限管理
- sentry: ログの集中管理
- alembic: テーブルマイグレーション

# Installations


# Notes
バッチ処理などで、サブディレクトリ配下のpyファイルから、別ディレクトリのファイルをimportする場合は、その前に以下のようなコードを追加して環境変数PYTHONPATHへの追加が必要
```
sys.path.append(str(Path(__file__).absolute().parent.parent))
```

