from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

from app.api.services.chat_model import generate_stream, generate_text
from app.api.routes.schemas.chat_bot_schema import InputSchema

chat_router = APIRouter(prefix="/chat")


@chat_router.post("/generate")
async def generate_chat_response(input: InputSchema):
    response = generate_text(input.text)
    return {"msg": response}


@chat_router.post("/stream-generate")
async def stream_chat_response(input: InputSchema):
    return StreamingResponse(
        generate_stream(input.text),
        media_type="text/plain",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
