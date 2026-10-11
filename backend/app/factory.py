from fastapi import FastAPI
from backend.app.core.config.settings import settings
def create_application() -> FastAPI:
    return FastAPI(title=settings.PROJECT_NAME)
