import sys
from pathlib import Path

import typer

sys.path.append(str(Path(__file__).parent.parent.absolute()))
import batch
import serve
import testing

from core.config import settings
from core.logger import init_logger

init_logger(settings.LOGGER_CONFIG_PATH)

app = typer.Typer()
app.add_typer(serve.app, name="serve")
app.add_typer(testing.app, name="testing")
app.add_typer(batch.app, name="batch")


if __name__ == "__main__":
    app()
