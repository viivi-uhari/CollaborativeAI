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

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to iteratively create a poem. 
            The details of the poem are as follows : {objective}
            Each User message will consist of the current status of the POEM and either a new line to the poem
            or a comment or question about the poem. 
            Discussion messages (comments or questions) will look like this:
            POEM : [ "This is Line one of the poem", "Line two follows in a run", "Line three is a bun" ]
            COMMENT : "I like the poem so far, it depicts a beautiful picture"
            New line messages will look like this:
            POEM : [ "This is Line one of the poem", "Line two follows in a run", "Line three is a bun" ]
            NEWLINE : "This line is for fun"
            When the user submits a new line message, you should also return a new line.
            When the user submits a discussion message, you should act as a helpful assistant in answering to the comment or question.
            """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        logger.info(request)
        linetag = "COMMENT" if request.inputData["comment"] else "NEWLINE"
        poemline = f"POEM : {json.dumps(request.inputData["poem"])}"
        newline = f"{linetag} : {request.text}"

        return TaskRequest(
            text=f"{poemline} \n{newline}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)