from typing import Any, List, Optional, Union, Literal
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

class ImageURL(BaseModel):
    url: str

class ImageMessage(OpenAIMessage):
    image_url: ImageURL
    model_config = ConfigDict(extra="ignore")


class TextMessage(OpenAIMessage):
    text: str
    model_config = ConfigDict(extra="ignore")

class Message(BaseModel):
    role: str 
    content: Union[str, List[Union[ImageMessage, TextMessage]]]
    model_config = ConfigDict(extra="ignore")
    
class InputMessage(Message):
    role: Literal["tool", "user", "assistant"] 


