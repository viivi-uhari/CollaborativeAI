import os

# define the Task
from task_examples import (
    poetry,
    tangram,
    gesture,
    openai_task,
    mealplan,
    tangram_openai,
    recipe,
    reference_list
)

currentTask = os.environ.get("TASK_NAME")

if currentTask == "tangram":
    task = tangram.Tangram()
elif currentTask == "openai":
    task = openai_task.OpenAITask()
elif currentTask == "gesture":
    task = gesture.Gesture()
elif currentTask == "poetry_openai":
    task = poetry.PoetryOpenAI()
elif currentTask == "mealplan":
    task = mealplan.Mealplan()
elif currentTask == "tangram_openai":
    task = tangram_openai.Tangram()
elif currentTask == "recipe":
    task = recipe.Recipe()
elif currentTask == "reference_list":
    task = reference_list.ReferenceList()
else:
    task = poetry.Poetry()
