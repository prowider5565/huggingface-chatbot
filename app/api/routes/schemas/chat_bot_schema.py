from pydantic import BaseModel


class InputSchema(BaseModel):
    text: str