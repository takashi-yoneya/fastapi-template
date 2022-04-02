import subprocess

import typer

app = typer.Typer()


@app.command()
def set_data():
    """
    テストデータのセット
    """
    print("test data")


if __name__ == "__main__":
    app()
