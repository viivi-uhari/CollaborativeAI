import logging
from tasks.task_interface import Task
import json
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)

logger = logging.getLogger(__name__)


class Recipe(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to give instruction for a food/meal recipe. 
            The user provides the recipe they want to make as follows: {objective}
            You will get a message from the user in the form COMMENT_LINE: COMMENT_LINE is the comment made by the user.
            Your answer must take the user's comment into consideration.
            Your recipe must be wrapped inside square brackets, along with some comments about the recipe that 
            you gave: (example: "[<the recipe>] <the comment>").
            The recipe must be formatted in JSON. Follows the form of this example:\n
            {{
              "name": "Spaghetti Bolognese",
              "ingredients:
                  {{ 
                    "olive_oil": "2 tbsp",
                    "onion": "1, finely chopped",
                    "garlic": "2 cloves, minced",
                    "carrot": "1, finely chopped",
                    "celery": "1 stalk, finely chopped",
                    "ground_beef": "500g",
                    "tomato_paste": "2 tbsp",
                    "canned_tomatoes": "400g, crushed",
                    "beef_broth": "250ml",
                    "red_wine": "125ml (optional)",
                    "dried_oregano": "1 tsp",
                    "dried_basil": "1 tsp",
                    "salt": "to taste",
                    "black_pepper": "to taste",
                    "bay_leaf": "1",
                    "milk": "100ml",
                    "spaghetti": "400g",
                    "parmesan_cheese": "to serve",
                    "fresh_basil": "to garnish" 
                  }}, 
              "instruction": 
                  {{ 
                      "Heat olive oil in a large pan over medium heat.",
                      "Add onion, garlic, carrot, and celery. Sauté until softened.",
                      "Increase heat, add ground beef, and cook until browned.",
                      "Stir in tomato paste, then add canned tomatoes, beef broth, red wine (if using), oregano, basil, salt, pepper, and bay leaf.",
                      "Reduce heat and let simmer for at least 30 minutes, stirring occasionally.",
                      "Add milk and stir well. Simmer for another 10-15 minutes.",
                      "Meanwhile, cook spaghetti according to package instructions. Drain well.",
                      "Remove bay leaf from the sauce and discard.",
                      "Serve sauce over spaghetti, topped with grated Parmesan and fresh basil."
                  }}
              "servings": 4,
              "prep_time": "15 minutes",
              "cook_time": "45 minutes",
              "total_time": "1 hour"
            }}
            If the user ask or request something, you answer it as a comment.
            You are curious, and always ready and eager to ask the user question if needed."""
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        logger.info(request)
        linetag = "COMMENT" if request.inputData["comment"] else "NEWRECIPE"
        plan = f"RECIPES : {json.dumps(request.inputData['recipes'])}"
        newplan = f"{linetag} : {request.text}"

        return TaskRequest(
            text=f"{plan} \n{newplan}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )
    
    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
    

    