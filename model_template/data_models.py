from pydantic import BaseModel, Field
from typing import List


class TaskMessage(BaseModel):
    role: str  # The role of the Message (either "assistant" or "user")
    content: str  # The content of the message


class TaskInput(BaseModel):
    text: List[TaskMessage]  # The history of the conversation
    image: bytes  # The image to be processed
    system: str  # A System message that indicates the Task


class TaskOutput(BaseModel):
    text: str = Field(default="")  # The response Message
    image: bytes = Field(default=None)  # The image to be processed
