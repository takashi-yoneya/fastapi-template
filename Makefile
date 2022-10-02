# コンテナ内に入る
.PHONY: docker-run
docker-run:
	docker compose run --rm web bash

# Docker内でファイルを作成・更新した場合に、ローカルで権限の問題になる場合の対応
.PHONY: chown
chown:
	sudo chown -hR ${USER}:${USER} .
