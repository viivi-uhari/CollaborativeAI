from fastapi import APIRouter, Depends, Request
from models import TaskDataRequest
from routers.session import get_session, clear_session
from tasks.tangram import build_model_request, convert_model_response
from typing import Dict
import logging
from gprc_server.queue_handler import queue_handler

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/task")




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


@router.delete("/finish")
async def clear_session(request: Request, session: Dict = Depends(get_session)):
    """Finish task endpoint:
    delete the session based on the session_id cookie when the user decides
    their task is done
    """
    clear_session(request)
    return {"response": "session cleared"}
