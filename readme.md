
バッチ処理などで、サブディレクトリ配下のpyファイルから、別ディレクトリのファイルをimportする場合は、その前に以下のようなコードを追加して環境変数PYTHONPATHへの追加が必要
```
sys.path.append(str(Path(__file__).absolute().parent.parent))
```