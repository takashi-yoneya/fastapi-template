import subprocess

import typer

from core.logger import get_logger

logger = get_logger(__name__)
print(__name__)

app = typer.Typer()


@app.command()
def batch1():
    """
    バッチ処理
    """
    print("batch1")
    logger.info("batch1")


if __name__ == "__main__":
    app()
