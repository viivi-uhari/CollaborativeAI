import logging
from tasks.task_interface import Task
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)

logger = logging.getLogger(__name__)


class Mealplan(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You take the role of a dietary expert and a good chef.
            You are working together with a user to iteratively create a meal plan. 
            The description of the diet are provbided by the user as follows : {objective}
            You will get a message from the user in the form MESSAGE: MESSAGE is the message that the user provide
            and it is wrapped inside square brackets. Your answer is your meal plan recommendation based on the description 
            provided by the user. Your answer must be a json string, and it should comply to the requirements given by the
            user such as amount of days, number of meals, nutritional values, dietary restriction. 
            In each of those day, the details of the meals must be presented.
            """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        logger.info(request)
        return TaskRequest(
            text=f"[COMMENT] : {request.text}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )
    
    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
    

    