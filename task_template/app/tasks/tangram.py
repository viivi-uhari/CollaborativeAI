import logging
import models
from typing import Any, List
import json
from grpc_server.task_interface import Task
import grpc_server.tasks_pb2 as grpc_models
from models import TaskDataRequest, TaskDataResponse

logger = logging.getLogger(__name__)


class Tangram(Task):
    

    def convert_task_data_to_tangram_data(task_data: Any) -> List[models.Piece]:
        pieces = []
        for piece in task_data:
            name, position_values = list(piece.items())[0]
            position = models.Position(
                x=position_values[0], y=position_values[1], rotation=position_values[2]
            )
            piece = models.Piece(name=name, position=position)
            pieces.append(piece)
        return pieces

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


    def generate_model_request(
        self, request : TaskDataRequest
    ) -> grpc_models.taskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        request = grpc_models.taskRequest()
        prompt_content = self.process_tangram_data(pieces)
        taskData = request.inputData
        pieces = self.convert_task_data_to_tangram_data(taskData)        
        system_prompt = self.get_system_prompt(request.objective)
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
