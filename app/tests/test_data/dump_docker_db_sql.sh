
PARENT_DIR=$(cd $(dirname $0);pwd)
echo $PARENT_DIR

# 定義のみ全てダンプ
 mysqldump -h 127.0.0.1 -P 3307 -u docker -pdocker --ssl-mode=DISABLED docker > $PARENT_DIR/dump.sql

# gz圧縮
gzip $PARENT_DIR/dump.sql -f