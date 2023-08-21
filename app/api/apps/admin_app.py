from fastapi import FastAPI

from app.api.endpoints import admin

app = FastAPI()
app.include_router(admin.router, prefix="/admin", tags=["admin"])
