import os

# define the Task
from task_examples import poetry, tangram


if os.environ.get("TASK_NAME") == "tangram":
    task = tangram.Tangram()
else:
    task = poetry.Poetry()
