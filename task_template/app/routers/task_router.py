from fastapi import APIRouter, Depends, Request
from models import TaskDataRequest
from routers.session import get_session, clear_session
from typing import Dict
import tasks
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/task")

availableTasks = {"tangram": tasks.tangram.call}


@router.post("/process")
async def process_task_data(
    task_data: TaskDataRequest, session: Dict = Depends(get_session)
):
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    result = await availableTasks[task_data.taskId](
        task_data.data, task_data.objective, session["history"], model()
    )
    logger.debug(result)
    return {"data": result}


@router.delete("/finish")
async def clear_session(request: Request, session: Dict = Depends(get_session)):
    """Finish task endpoint:
    delete the session based on the session_id cookie when the user decides
    their task is done
    """
    clear_session(request)
    return {"response": "session cleared"}
