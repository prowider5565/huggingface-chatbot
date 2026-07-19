from pydantic import BaseModel


class InputSchema(BaseModel):
    message: str
