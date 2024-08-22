# Collaborative AI Arena

The collaborative AI arena is intended to serve as a basis for evaluation of collaboration between AI and Humans. The idea is to design and evaluate tasks which are performed with input from both sides, and figure out if the collaboration was successful.
Users should be presented with a task that they perform together with the AI and metric should be used to evaluate the different

This repository contains most of the code necessary to add a Model or a Task.

## Task Templates:

There are two tasks, `poetry` and `tangram` currently available as examples. Poetry has a frontend created in ReactJS and tangram in vueJS using a godot game.

### Prompt:

The prompt for the tasks are located at `task_template/app/task_examples` For poetry, the task is in [poetry.py](task_template/app/task_examples/poetry.py)
for the tangram task it is located in [tangram.py](task_template/app/task_examples/tangram.py)
Although the current prompts serve as a starting point for the tasks, they are by no means optimized. Because of that, we highly recommend you to experiment and do some prompt engineering for it to fit whatever task you have in mind.

## Frontend:

There are two example frontends. One is for a poetry task done in ReactJS, the other is for a tangram game using vueJS and a godot game.

### Poetry

The main idea of the task is that the user submits the theme/objective for the poem and then they collaborate with the model to complete it. However, This task is not limited to poem writing only as you can freely switch between a line-by-line rendering (poem) or a continuous rendering (paragraph). For a more detailed explanation, please go [here](task_template/frontend_poetry/README.md)

### Tangram

The idea is that the human and the AI work together to build something with a tangram game. At the moment the game provided is restricted to two pieces, so there iis only a limited amount of options. The game can be replaced by whatever the user wants, and just represents one possibility.
For a more detailed explanation, please go [here](task_template/frontend_tangram/README.md)

## Model selection:

At the moment, the system supports two models [gpt4-turbo](model_template/models/openAI_model.py) and [gpt4-o](model_template/models/openAI_image_model.py), which are located inside the folder [model_template/models](model_template/models).

You can change between the two models by changing the value of the variable `ai_model` between `OpenAIImageModel()` and `OpenAIModel()` in the file [model_template/model.py](model_template/model.py).
If you have time and want to add your own models to the system, feel free to do so by following the template located in the file [basemodel.py](model_template/models/basemodel.py) and using the already existing model files as guidance.

## Templates

The `task_template` and `model_template` folders contain template applications for deployment on the AI Builder infrastructure.
They indicate how to implement a model and a task and supply most infrastructure necessary to minimise the requirements of a user to adopt their code.
Details are provided in the respective README files.

## Local testing

To test things locally and see if they work, we provide a docker compose file along with a simple orchestrator.

To run locally you will need docker installed!

To run, you need docker installed.  
You also need the following environment variables set:

- `OPENAI_API_KEY` - a openAI access key.
- `SSL_KEY` - a valid openssl certficate key
- `SSL_CERTIFICATE` - a valid openssl certificate

The template model currently uses an Aalto specific endpoint for computation.
You will likely need to change the model used in `model_template/model.py` to an OpenAI model and use that for testing.

We provide two tasks that can be used, either a poetry task or a tangram task. To run them call:
`docker compose -f docker-compose_tangram.yaml up --build` for the tangram task and  
`docker compose -f docker-compose_poetry.yaml up --build` for the poetry task respectively
only one of the tasks can be run at the same time.

After that, the frontend should be accessible via https://localhost:8062.
