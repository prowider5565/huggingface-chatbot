from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.api.routes import chat_bot, health, pages
from app.api.services.bootstrap import initialize
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
    app.include_router(health.router, prefix=settings.api_v1_prefix)
    app.include_router(chat_bot.chat_router, prefix=settings.api_v1_prefix)
    app.include_router(pages.router)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    return app


app = create_app()
