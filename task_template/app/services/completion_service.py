from fastapi import APIRouter, Depends, Request
from models import (
    TaskDataRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
    TaskMetrics,   
    TaskRequest         
)
from routers.router_models import (
    ConversationItem,    
    SessionData,
    OpenAIChatBaseModel,
    TextMessage,
    ImageMessage,
    Message,
    ImageURL
)
from routers.session import get_session, clear_session
from typing import Dict, List
from tasks.task_interface import Task
import asyncio
import logging
from grpc_server.queue_handler import queue_handler
import grpc_server.tasks_pb2 as grpc_models
from datetime import datetime
from tasks.task import task
import json

logger = logging.getLogger(__name__)

class CompletionService:
    def __init__(self):        
        self.task = task
        logger.info(f"Task set to {self.task}")

    def get_requirements(self) -> TaskRequirements:
        return self.task.get_requirements()

    def build_model_request(
        self, request: TaskDataRequest, history: List[ConversationItem]
    ) -> grpc_models.taskRequest:
        currentElement = self.task.generate_model_request(request)
        grpc_taskRequest = grpc_models.taskRequest()
        # Extend the history by the current request.
        logger.info(currentElement.text)                
        # Now, convert this into the grpc request
        messages = [Message(role="user", content=element.text) for element in history]
        currentMessage = Message(role="user", content=[TextMessage(type="text", text=currentElement.text)])

        if currentElement.image:
            currentMessage.content.append(ImageMessage(type="image_url", image_url=ImageURL(url=currentElement.image)))
        messages.append(currentMessage)        
        # Store it in the history, if this version is used, we do not store images.
        history.append(ConversationItem(role="user", content=currentElement.text))
        grpc_taskRequest = grpc_models.taskRequest()   
        grpc_taskRequest.request = json.dumps([message.model_dump() for message in messages])
        return grpc_taskRequest

    def build_model_request_from_open_AI_request(self,messages : OpenAIChatBaseModel):
        grpc_taskRequest = grpc_models.taskRequest()   
        grpc_taskRequest.request = json.dumps(messages.model_dump()["messages"])
        return grpc_taskRequest

    def build_open_AI_response( self, response: grpc_models.modelAnswer, messageID : str):
            data = ModelResponse.model_validate_json(response.answer)            
            choices = [
                {
                    "index": 0,
                    "logpobs": None,
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": data.text},
                }
            ]
            openAIResponse = {
                "id": "chatcmpl-123456",
                "object": "chat.completion",
                # timestamp in ms
                "created": datetime.now().timestamp(),
                "model": "unknown",
                "choices": choices,
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "total_tokens": 2,
                },
                "system_fingerprint": messageID,
            }
            return openAIResponse
        

    def interpret_model_response(
        self, response: grpc_models.modelAnswer, history: List[ConversationItem]
    ) -> TaskDataResponse:
        # Load the json
        logger.info(response)
        logger.info(response.answer)
        data = ModelResponse.model_validate_json(response.answer)
        history.append({"role": "assistant", "content": data.text})
        return self.task.process_model_answer(data)
