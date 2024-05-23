# Collaborative AI Arena

The collaborative AI arena is intended to serve as a basis for evaluation of collaboration between AI and Humans. The idea is to design and evaluate tasks which are performed with input from both sides, and figure out if the collaboration was successful.
Users should be presented with a task that they perform together with the AI and metric should be used to evaluate the different

This repository contains most of the code necessary to add a Model or a Task.

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
