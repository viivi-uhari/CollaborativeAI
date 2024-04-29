from typing import Any, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class TaskDataRequest(BaseModel):
    text: str
    inputData: Any
    image: Optional[str] = None
    objective: str

class TaskDataResponse(BaseModel):
    text: str    
    image: Optional[str] = None    


class textHistory(BaseModel):
    role: str
    content: str


class modelRequest(BaseModel):
    text: List[textHistory]
    image: str
    system: str
