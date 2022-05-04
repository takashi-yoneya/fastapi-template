
PARENT_DIR=$(cd $(dirname $0);pwd)
echo $PARENT_DIR

# 定義のみ全てダンプ
mysqldump -h 127.0.0.1 -P 3307 -u docker -pdocker --ssl-mode=DISABLED --no-tablespaces --skip-add-locks docker > $PARENT_DIR/dump.sql
mysqldump -h 127.0.0.1 -P 3307 -u docker -pdocker --ssl-mode=DISABLED --no-tablespaces --skip-add-locks docker > $PARENT_DIR/dump.structure.sql

# gz圧縮
gzip $PARENT_DIR/dump.sql -f