from models import TaskDataRequest
from routers.session import get_session, sessions
from typing import Dict
import logging

logger = logging.getLogger(__name__)

"""
example of a TaskDataRequest
    {
        "taskID": 1,
        "data": {
            "pieces": [
                {
                    "id": "Big_triangle_1",
                    "shape": "triangle",
                    "size": "Big",
                    "color": "red",
                    "position": ...
                },
                ...
            ]
        },
        "objective": "make a boat"
    }
"""


def process_tangram_data(tangram_data):
    logger.debug(tangram_data)
    requestData = tangram_data["data"]["tangramData"]
    for piece in requestData.keys():
        if piece == "Big Triangle 1":
            large_triangle_1 = requestData[piece]
        elif piece == "Big Triangle 2":
            large_triangle_2 = requestData[piece]
        elif piece == "Medium Triangle":
            medium_triangle = requestData[piece]
        elif piece == "Small Triangle 1":
            small_triangle_1 = requestData[piece]
        elif piece == "Small Triangle 2":
            small_triangle_2 = requestData[piece]
        elif piece == "Square":
            square = requestData[piece]
        else:
            parallelogram = requestData[piece]

    prompt = f"""
        Here are the current positions and rotations of the pieces:
        Big Triangle 1: {large_triangle_1[0:1]}
        Big Triangle 2: {large_triangle_2[0:1]}
        Medium Triangle: {medium_triangle[0:1]}
        Small Triangle 1: {small_triangle_1[0:1]}
        Small Triangle 2: {small_triangle_2[0:1]}
        Square: {square[0:1]}
        Parallelogram: {parallelogram[0:1]}        
    """
    return prompt


async def call(data, objective, history, modelID: str):
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """

    prompt = process_tangram_data(data)
    logger.debug(prompt)

    # Model ID will need to be changed at some point to allow non GPT/openAI models
    response = await get_model_response(history, objective, model)
    history.append(response)
    # Post process response:
    response_message = "{" + response.content + "}"
    # assuming the response the model gives follows the template and return a json string
    return {"tangram": response_message}


async def get_model_response(prompt, objective: str, model: BaseLLM):
    """Generate response endpoint:
    generate the response based on given prompt and store the conversation
    in the history of the session (based on the session_id cookie)
    """

    system_prompt = f"""
        Your are working with a user to solve some task with a tangram puzzle. 
        The stated task is : {objective}
        You will be given central points for the objects of the tangram puzzle.         
        The corners of the objects are as follows (relative to their central points):
        1. Big Triangle 1: (-85,-85), (-85,85), (95,95)
        2. Big Triangle 2: (-96,-96),(-96,85),(85,85)
        3. Medium Triangle: (0,0), (0,128), (128,128)
        4. Small Triangle 1: (-45,-45),(-45,45),(45,45)
        5. Small Triangle 2: (-45,-45),(-45,45),(45,45)
        6. Square: (-45,-45), (-45,45), (45,45), (45,-45)
        7. Parallelogram: (-40,-24), (88,-24), (24, 40), (-104,40)
        The information you will get, are the central points along with a rotation (in degrees) s follows:
        ["(4,5)",45]
        You should only modify one piece in each of your turns. A Move can consist of both roatting and movig the piece.
        You should respond with the new location and rotation of the element you modified in the following format, 
        similar to the positions provided by the user. 
        "Piece Name" : ["(x,y)", rotation]
        Your answer must only contain one line.
        """
    res = model([SystemMessage(content=system_prompt)] + prompt)
    return res
