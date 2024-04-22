import logging
import models
from typing import Any, List, Optional
from gprc_server.queue_handler import queue_handler
import json

logger = logging.getLogger(__name__)


def process_tangram_data(pieces: List[models.Piece]):
    prompt = "Here are the current positions and rotations of the pieces:\n"
    for piece in pieces:
        prompt += f"{piece.name}: {piece.position.x}, {piece.position.y}, {piece.position.rotation}\n"
    return prompt


def convert_model_response(response: Any) -> models.Piece:
    try:
        element = json.loads(response)
        name, position_values = list(element.items())[0]
        position = models.Position(
            x=position_values[0], y=position_values[1], rotation=position_values[2]
        )
        piece = models.Piece(name=name, position=position)
        return piece
    except:
        logger.error("Error converting model response to Piece")
        return None


async def build_model_request(
    pieces: List[models.Piece], objective: str, history: List, image: str
) -> models.modelRequest:
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    prompt_content = process_tangram_data(pieces)
    system_prompt = get_system_prompt(objective)
    prompt = {"role": "user", "content": prompt_content}
    model_request = models.modelRequest(
        text=history.extend([prompt]), image=image, system=system_prompt
    )
    return model_request


def get_system_prompt(objective: str, hasImage: bool = False) -> str:
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
        The information you will get, are the central points along with a rotation (in degrees) as follows:
        [4,5,45]
        You should only modify one piece in each of your turns. A move can consist of both roatting and movig the piece.
        You should respond with the new location and rotation of the element you modified in the following format, 
        similar to the positions provided by the user. 
        {"Piece Name" : [x,y, rotation]}
        Your answer must only contain one line.
        """
    return system_prompt
