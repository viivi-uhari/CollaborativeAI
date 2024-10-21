import os

# define the Task
from task_examples import poetry, tangram, openai_task


if os.environ.get("TASK_NAME") == "tangram":
    task = tangram.Tangram()
if os.environ.get("TASK_NAME") == "openai_task":
    task = openai_task.OpenAITask()
else:
    task = poetry.Poetry()
