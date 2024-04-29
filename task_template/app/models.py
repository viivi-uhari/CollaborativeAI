from typing import Any, List, Optional
from pydantic import BaseModel


class TaskDataRequest(BaseModel):
    text: str
    inputData: Any
    image: Optional[str] = None
    objective: str


class TaskRequest(BaseModel):
    # The text of the request
    text: str
    # the image of the request
    image: Optional[str] = None
    # The system message of the request
    system: str


class ModelResponse(BaseModel):
    # The text of the request
    text: str
    # the image of the request
    image: Optional[str] = None


class TaskDataResponse(BaseModel):
    text: str
    image: Optional[str] = None
