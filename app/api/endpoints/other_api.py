from fastapi import APIRouter

from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/hoge", operation_id="get_other_hoge")
async def get_other_hoge() -> dict[str, str]:
    return {"response": "hoge"}
