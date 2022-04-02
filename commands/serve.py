import subprocess

import typer

app = typer.Typer()


@app.command()
def run():
    """
    FastAPIサーバーの起動(uvicorn)
    """
    subprocess.run("uvicorn main:app --host 0.0.0.0 --reload --log-config logger_config.yaml")


if __name__ == "__main__":
    app(run)
