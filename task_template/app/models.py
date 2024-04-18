from typing import Any, List
from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str
    
class TaskDataRequest(BaseModel):
    taskId : str 
    data: Any 
    objective: str

class SessionData(BaseModel):
    '''
    I dont know yet if we're going to use AI Builder for the demo. If we are then I think we need to
    provide the apiKey to the session and then extract it to make the call. If not, we can just use the
    api key from the .env file
    '''
    apiKey: str
    modelId: str
    history: List[dict] = []