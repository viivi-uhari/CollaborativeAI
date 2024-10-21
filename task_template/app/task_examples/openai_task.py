import logging
from typing import Any, List
import json
from tasks.task_interface import Task
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)

logger = logging.getLogger(__name__)


class Poetry(Task):

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        return TaskRequest(
            text=request.text,
            system=request.objective,
            image=request.image,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=True)
