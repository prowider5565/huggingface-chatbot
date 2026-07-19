from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"app_name": settings.app_name})
