from fastapi import FastAPI

from app.api.endpoints import other_api

app = FastAPI()
app.include_router(other_api.router, prefix="/other", tags=["other"])
