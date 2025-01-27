import os

# define the Task
from task_examples import poetry, tangram, gesture, openai_task, mealplan


if os.environ.get("TASK_NAME") == "tangram":
    task = tangram.Tangram()
elif os.environ.get("TASK_NAME") == "openai":
    task = openai_task.OpenAITask()
elif os.environ.get("TASK_NAME") == "gesture":
    task = gesture.Gesture()
elif os.environ.get("TASK_NAME") == "mealplan":
    task = mealplan.Mealplan()
else:
    task = poetry.Poetry()
