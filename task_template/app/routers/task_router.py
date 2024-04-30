from fastapi import APIRouter, Depends, Request
from models import TaskDataRequest, TaskDataResponse, ModelResponse
from routers.router_models import ConversationItem, TaskRequest
from routers.session import get_session, clear_session
from typing import Dict, List
from tasks.task_interface import Task
import asyncio
import logging
from grpc_server.queue_handler import queue_handler
import grpc_server.tasks_pb2 as grpc_models

logger = logging.getLogger(__name__)
task_router = APIRouter(prefix="/api/v1/task")


class TaskRouter:
    def _init__(self):
        pass

    def set_Task(self, task: Task):
        self.task = task

    def build_model_request(
        self, request: TaskDataRequest, history: List[ConversationItem]
    ) -> grpc_models.taskRequest:
        currentElement = self.task.generate_model_request(request)
        grpc_taskRequest = grpc_models.taskRequest()
        # Extend the history by the current request.
        history.extend(currentElement.text)
        # Now, we convert this into the taskRequest
        currentRequestObject = TaskRequest(
            text=history, image=currentElement.image, system=currentElement.system
        )
        grpc_taskRequest.request = currentRequestObject.model_dump_json()
        return grpc_taskRequest

    def interpret_model_response(
        self, response: grpc_models.modelAnswer
    ) -> TaskDataResponse:
        # Load the json
        data = ModelResponse().load_json(response.answer)
        return self.task.process_model_answer(data)


task_handler = TaskRouter()


@task_router.post("/process")
async def process_task_data(
    task_data: TaskDataRequest, session: Dict = Depends(get_session)
):
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    history = session["history"]
    sessionID = session["key"]
    if not sessionID in queue_handler.response_queues:
        queue_handler.start_queue.put(sessionID)

    # Wait for the response queue to be created
    while not sessionID in queue_handler.response_queues:
        await asyncio.sleep(1)
    # Submit the task to the model
    model_request = task_handler.build_model_request(task_data, history)
    queue_handler.task_queue.put({"data": model_request, "sessionID": sessionID})

    # And wait for the response to arrive:
    while True:
        if queue_handler.response_queues[sessionID].empty():
            await asyncio.sleep(1)
        else:
            ret = queue_handler.response_queues[sessionID].get(block=True)
            update = task_handler.interpret_model_response(ret)
            return update


@task_router.delete("/finish")
async def clear_session(request: Request, session: Dict = Depends(get_session)):
    """Finish task endpoint:
    delete the session based on the session_id cookie when the user decides
    their task is done
    """
    clear_session(request)
    return {"response": "session cleared"}
