# Model template for use with the Collaborative AI Arena

This model serves as a template model ( and as a suggestion on how to set up communication pathes)
The aim of this model template is to allow concurrent processing of requests and implement the flow for the Model component as detailed in the following diagram:

![A diagram showing the flow of messages from the model perspective](docs/threecomp_layout.svg)

## Model Messages

There are four types of messages, a will receive or send, which are all defined by the `model.proto` file.
The messages along with their fields are:

- Incoming Messages
  - `modelRequest`
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.
      - `system`: A String representing a system message to the model (i.e. the task description)
    - `modelID`: A string representing which model this request is for
    - `sessionID`: An ID of the session that generated this resource
  - `metricsJson`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `modelID`: A string representing which model this request is for
- Outgoing Messages:
  - `modelDefinition`:
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `can_text`: A Bool indicating whether the model can handle text
    - `can_image`: A Bool indicating whether the model can handle images
    - `modelID`: The ID of this model
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields:
      - `text` : The text of the answer of the model
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that prompted this response

## Model Services

The model will need to implement the four services detailed in the model.proto file.
Those contain:

- `registerModel` : A Service which is called with an empty request on startup and need to send one single message contiaining the `modelDefinition`. This definition indicates the capailities of the model (i.e. if it can process images and text, and if it needs images/text for processing, or, if false, if it can work without them, one should always be prvided). Along with the deifnition, the model needs to specify a model ID which it can use to determine whether a future request is for this model or not.
- `predict` : A Service that receives requests for the model to perform a prediction with. The request is accompanied by a `sessionID` which is required in the response and a `modelID`. The latter is an indicator whether this message is for the current model. If the `modelID` provided does not fit the ID it provided it should do nothing
- `sendPrediction` This service should send messages of type `modelResponse` for each successfully handled `modelRequest`. These `modelAnswers` need to contain the `sessionID` that was provided in the request in order to allow them to be asssociated with the correct model
- `publishMetrics`: this endpoint receives a `modelMetrics` message and then, either handles it, if the contained `modelID` matches this models `modelID` or ignors it.

## Implementation

We provide a sample implementation of a model server in the model_server.py class.

### Models:

For simplicty, we have defined three pydantic models, that we use for interaction between the model server and the actual model implementation in the data_models class:

- `TaskMessage`, a class with two fields:
  - `role` : A String indicating the role that generated the element (either "user" for the participant or "assistant" for the ai )
  - `content`: the content of the message
- `TaskInput`, a class defining the input to a task

  - `text` : a List of `TaskMessage` objects (representing the textual history)
  - `image` : a string base64 encoded image
  - `system` : The system message describing the task to solve

- `TaskOutput`, a class defining the input to a task
  - `text` : a String with the model answer
  - `image` : a string base64 encoded image of the model answer (can be None)

### Interface

This server handles most interactions and relies on the AIModel class defined in the `model.py` file to provide the following methods and fields:

- Methods:
  - publish_metrics(metrics_json: str):
    - A Method that publishes (i.e. prints) the given metrics to the container log
  - async get_response(message: TaskInput) -> TaskOutput:
    - A asynchronous method that performs the handling of the input, processing it by the actual model and returning a TaskOutput that can then be sent on.
  - get_model_definition() -> model_pb2.modelDefinition:
    - Indicate the `modelDefinition`, i.e. its capabilities and requirements as defined above in the outgoing message list.
