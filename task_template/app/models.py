from typing import Any, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class Position(BaseModel):
    x: float
    y: float
    rotation: int


class Piece(BaseModel):
    name: str
    position: Position


class TaskDataRequest(BaseModel):
    comment: Optional[str] = ""
    pieces: List[Piece]
    image: Optional[str] = None
    objective: str


class SessionData(BaseModel):
    """
    I dont know yet if we're going to use AI Builder for the demo. If we are then I think we need to
    provide the apiKey to the session and then extract it to make the call. If not, we can just use the
    api key from the .env file
    """

    apiKey: str
    modelId: str
    history: List[dict] = []


class textHistory(BaseModel):
    role: str
    content: str


class modelRequest(BaseModel):
    text: List[textHistory]
    image: str
    system: str
