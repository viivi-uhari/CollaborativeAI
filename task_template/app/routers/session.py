from fastapi import Depends, Request, APIRouter
from typing import Dict
import time
import hashlib
from models import SessionData
import random
import grpc
import logging

4
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/session")
channel = grpc.insecure_channel("localhost:8061")

# Mock up sessions db
sessions: Dict[str, SessionData] = {}
'''
sessions[<session_id>] = {
  "apiKey": <apiKey>, #if there are no way to store secret in AI builder then we might need to get it from the session
  "modelId": <modelId>
  "history": [
    {
      "role": "system", 
      "content": """ You are a helpful assistant. The user want to solve the tangram puzzle to create some 
                      kind of shape. You are collaborating with the user in order to help them achieve that task. """
    },
    {
      "role": "user"
      "content": <prompt>
    }
  ]
}
'''


def get_session(request: Request):
    session_id = request.session["key"] if "key" in request.session else None
    if session_id is None or session_id not in sessions:
        session_id = hashlib.sha256(
            (request.client.host + str(time.time())).encode()
        ).hexdigest()
        request.session["key"] = session_id
        sessions[session_id] = {
            "apiKey": "",
            "history": [],
        }
    return sessions[session_id]


def clear_session(request: Request):
    session_id = request.session["key"] if "key" in request.session else None
    if session_id is None or session_id not in sessions:
        pass
    else:
        sessions.pop(session_id)
        return True


########################################## for testing purpose ##########################################
@router.get("/modelId")
async def get_items(session: Dict = Depends(get_session)):
    return {"modelId": session["modelId"]}


@router.post("/modelId")  # set the model for the openai call
async def update_model_id(modelId: str, session: Dict = Depends(get_session)):
    session["modelId"] = modelId
    return {"response": f"model id is updated ({modelId})"}


@router.get("/")  # can be used to generate a session
async def get_session_info(session: Dict = Depends(get_session)):
    logger.info("Session was requested. Returning session info.")
    logger.info(session)
    return session


@router.get("/history")
async def get_items(session: Dict = Depends(get_session)):
    return {"history": session["history"]}


@router.get("/sessions")
async def get_items(session: Dict = Depends(get_session)):
    return {"session-id": sessions}


@router.delete("/sessions")
async def get_items():
    sessions.clear()
    return {"response": "sessions cleared"}
