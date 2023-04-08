# コンテナ内に入る
.PHONY: docker-run
docker-run:
	docker compose run --rm web bash

# Docker内でファイルを作成・更新した場合に、ローカルで権限の問題になる場合の対応
.PHONY: chown
chown:
	sudo chown -hR ${USER}:${USER} .


.PHONY: openapi-generator
openapi-generator:
	docker compose run --rm openapi-generator


.PHONY: makemigrations
makemigrations:
	docker compose run --rm web bash -c "poe makemigrations"


.PHONY: migrate
migrate:
	docker compose run --rm web bash -c "poe migrate"

.PHONY: drop-all-tables
drop-all-tables:
	docker compose run --rm web bash -c "poe drop-all-tables"

.PHONY: pre-commit-all
pre-commit-all:
	pre-commit run --all-files

.PHONY: pre-commit-update
pre-commit-update:
	pre-commit autoupdate

.PHONY: export-requirements-txt
export-requirements-txt:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: export-requirements-dev-txt
export-requirements-dev-txt:
	poetry export -f requirements.txt --output requirements-dev.txt --dev

.PHONY: test
test:
	docker compose run --rm web bash -c "poe test"
