from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.api.routes.schemas.chat_bot_schema import InputSchema
from app.api.services.chat_model import generate_stream, generate_text
from app.db.models import Message
from app.db.session import get_db

chat_router = APIRouter(prefix="/chat")


@chat_router.post("/generate")
async def generate_chat_response(input: InputSchema, db: Session = Depends(get_db)):
    db.add(Message(message=input.message))
    db.commit()
    response = generate_text(input.message)
    return {"msg": response}


@chat_router.post("/stream-generate")
async def stream_chat_response(input: InputSchema, db: Session = Depends(get_db)):
    db.add(Message(message=input.message))
    db.commit()
    return StreamingResponse(
        generate_stream(input.message),
        media_type="text/plain",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
