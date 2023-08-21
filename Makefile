# コンテナ内に入る
.PHONY: docker-run
docker-run:
	@docker compose run --rm web bash

# Docker内でファイルを作成・更新した場合に、ローカルで権限の問題になる場合の対応(ubuntuの場合)
.PHONY: chown
chown:
	@sudo chown -hR ${USER}:${USER} .

# フロントエンド用のAPIClientを生成
.PHONY: openapi-generator
openapi-generator:
	@docker compose run --rm openapi-generator

# 全てのファイルに対してpre-commitを実行
.PHONY: pre-commit-all
pre-commit-all:
	@pre-commit run --all-files

# pre-commitで指定されているパッケージのバージョンを更新
.PHONY: pre-commit-update
pre-commit-update:
	@pre-commit autoupdate

# pytestでテストを実行
.PHONY: test
test:
	@docker compose run --rm web bash -c "pytest tests/ --durations=5 -v"

# マイグレーションファイルを作成
# m: マイグレーションファイルの名前
.PHONY: makemigrations
makemigrations:
	@docker compose run --rm web bash -c "alembic revision --autogenerate -m ${m}"

# DBのマイグレーション
.PHONY: migrate
migrate:
	@docker compose run --rm web bash -c "alembic upgrade heads"

# Seedデータの投入
.PHONY: seeder
seeder:
	@docker compose run --rm web bash -c "python seeder/run.py import_seed"

# 全てのテーブルの削除
.PHONY: drop-all-tables
drop-all-tables:
	@docker compose run --rm web bash -c "python seeder/run.py drop_all_tables"

# dbの初期化
.PHONY: init-db
init-db:
	@make drop-all-tables
	@make migrate
	@make seeder
