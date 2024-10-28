from typing import Any, List, Optional, Union
from pydantic import BaseModel, ConfigDict


class ConversationItem(BaseModel):
    role: str
    content: str


class SessionData(BaseModel):
    history: List[ConversationItem]
    id: str


class TaskRequest(BaseModel):
    text: List[ConversationItem]
    image: Optional[str] = None
    system: str


class OpenAIMessage(BaseModel):
    type: str


class ImageMessage(OpenAIMessage):
    url: str
    model_config = ConfigDict(extra="ignore")


class TextMessage(OpenAIMessage):
    text: str
    model_config = ConfigDict(extra="ignore")


class Message(BaseModel):
    role: str
    content: Union[str, List[Union[ImageMessage, TextMessage]]]
    model_config = ConfigDict(extra="ignore")


class OpenAIChatBaseModel(BaseModel):
    messages: Optional[List[Message]] = None
    model_config = ConfigDict(extra="ignore")
