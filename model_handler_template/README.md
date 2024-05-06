# Model handler documentation

This module serves as a handler that manages the connection between multiple models and tasks components. This documentation is for your information only. 

## Model Handler Messages

There are eight types of messages, which are all defined by the `model_handler.proto` file.
The messages along with their fields are:

- Incoming Messages
  - `modelRequirements`: A message that indicates, what the model needs to be able to handle for this session of this task
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `sessionID`: The ID for these requirements
  - `taskMetrics`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `sessionID`: The session for which these metrics were generated
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields:
      - `text` : The text of the answer of the model
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that prompted this response
  - `taskRequest`:
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.
      - `system`: A String representing a system message to the model (i.e. the task description)
    - `sessionID`: An ID of the session that generated this resource
  - `modelDefinition`:
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `can_text`: A Bool indicating whether the model can handle text
    - `can_image`: A Bool indicating whether the model can handle images
    - `modelID`: The ID of this model
- Outgoing Messages:
  - `modelRequest`:
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.
      - `system`: A String representing a system message to the model (i.e. the task description)
    - `modelID`: A string representing which model this request is for
    - `sessionID`: An ID of the session that generated this resource
  - `metricsJson`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `modelID`: A string representing which model this request is for
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields:
      - `text` : The text of the answer of the model
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that prompted this response

## Model Handler Services

