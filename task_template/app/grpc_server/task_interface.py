from grpc_server.queue_handler import QueueHandler
from models import TaskDataRequest, TaskDataResponse
import grpc_server.tasks_pb2 as gprc_models

class Task():
    def __init__(self, queue_handler : QueueHandler ):
        pass

    def generate_model_request(self, request : TaskDataRequest) -> gprc_models.taskRequest:
        raise NotImplementedError()
    
    def process_model_answer(self, answer : gprc_models.modelAnswer) -> TaskDataResponse:
        raise NotImplementedError()