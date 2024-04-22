from fastapi import APIRouter, Depends, Request
from models import TaskDataRequest
from routers.session import get_session, clear_session
from tasks.tangram import build_model_request, convert_model_response
from typing import Dict
import queue
import tasks
import logging
from gprc_server.queue_handler import queue_handler

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/task")


@router.post("/starttask")
def start_task(request: Request, task_data: TaskDataRequest):
    """Start task endpoint:
    start a new session based on the task data
    """
    session = get_session(request)
    sessionID = session["key"]
    # Set up the response Queue
    queue_handler.add_response_queue(sessionID)
    queue_handler.start_queue.put({"session": sessionID})
    return {"response": "task started"}


@router.post("/process")
async def process_task_data(
    task_data: TaskDataRequest, session: Dict = Depends(get_session)
):
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    history = session["history"]
    sessionID = session["key"]

    queue = queue_handler.task_queue.put(sessionID)
    model_request = build_model_request(
        task_data.pieces, task_data.objective, history, task_data.image
    )
    queue.put({"data": model_request, "sessionID": sessionID})
    return {"received": True}


@router.get("/update")
async def get_model_update(session: Dict = Depends(get_session)):
    """Get model update endpoint:
    get the model's response to the user's input
    """
    sessionID = session["key"]
    current_queue = queue_handler.get_response_queue(sessionID)
    ret = None
    if current_queue.empty():
        return {"status": "waiting"}
    else:
        ret = current_queue.get(block=True)
        update = convert_model_response(ret)
        return update


@router.delete("/finish")
async def clear_session(request: Request, session: Dict = Depends(get_session)):
    """Finish task endpoint:
    delete the session based on the session_id cookie when the user decides
    their task is done
    """
    clear_session(request)
    return {"response": "session cleared"}
