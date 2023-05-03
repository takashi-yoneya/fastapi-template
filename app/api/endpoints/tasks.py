import asyncio
import time

from fastapi import APIRouter, BackgroundTasks

from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


def long_process_thread(id: str) -> None:
    for i in range(100):
        logger.info(f"[long_process_thread(id={id})] {i+1}sec")
        time.sleep(1)


async def long_process_async(id: str) -> None:
    for i in range(100):
        logger.info(f"[long_process_asyncio(id={id})] {i+1}sec")
        await asyncio.sleep(1)


@router.post("/long-process/thread")
def exec_long_process_thread(
    id: str, background_tasks: BackgroundTasks,
) -> None:
    background_tasks.add_task(long_process_thread, id)


@router.post("/long-process/async")
async def exec_long_process_async(
    id: str, background_tasks: BackgroundTasks,
) -> None:
    background_tasks.add_task(long_process_async, id)
