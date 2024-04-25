from grpc import StatusCode
import grpc.aio as grpc
from concurrent import futures
import time

# import the generated classes :
import model_pb2
import model_pb2_grpc

# import the function we made :
import model as ai_model
import json
import asyncio
import queue
from data_models import TaskInput

port = 8061

model_definition = ai_model.model_definition


# create a class to define the server functions, derived from
class ModelServicer(model_pb2_grpc.ModelServicer):
    def __init__(self):
        self.start_queue = queue.Queue()
        self.result_queue = queue.Queue()

    def publishMetrics(self, request, context):
        if model_definition.modelID != request.modelID:
            # Not sure, whether we need to abort, as this might caus esome unexpected error.
            # This is just not connected to anything...
            # context.abort(StatusCode.UNIMPLEMENTED, "You've reached the wrong service.")
            return model_pb2.Empty()
        # We will just have the model print the metrics
        ai_model.publish_metrics(request.metrics)
        return model_pb2.Empty()

    def predict(self, request, context):

        if model_definition.modelID != request.modelID:
            # Not sure, whether we need to abort, as this might caus esome unexpected error.
            # This is just not connected to anything...
            # context.abort(StatusCode.UNIMPLEMENTED, "You've reached the wrong service.")
            return model_pb2.Empty()
        # define the buffer of the response :
        # get the value of the response by calling the desired function :
        self.start_queue.put(request)
        return model_pb2.Empty()

    async def do_prediction(self, data: model_pb2.modelRequest):
        input = TaskInput.model_validate_json(data.request)
        result = await ai_model.get_response(input)
        modelAnswer = model_pb2.modelAnswer()
        modelAnswer.response = result.model_dump_json()
        modelAnswer.sessionID = data.sessionID
        self.result_queue.put(modelAnswer)

    async def process_queue(self):
        while True:
            if self.start_queue.empty():
                await asyncio.sleep(1)
            else:
                data = self.start_queue.get(timeout=1.0)
                task = asyncio.create_task(self.do_prediction(data))

    async def sendPrediction(self, request, context):
        _ = request
        print("Starting prediction queue")
        task = asyncio.create_task(self.process_queue(context))
        while True:
            if self.done_queue.empty():
                await asyncio.sleep(1)
            else:
                data = self.done_queue.get(timeout=1.0)
                yield data

    def registerModel(self, request, context):
        # get the value of the response by calling the desired function :
        return model_definition


async def serve():
    # create a grpc server :
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ModelServicer_to_server(ModelServicer(), server)
    print("Starting server. Listening on port : " + str(port))
    server.add_insecure_port("0.0.0.0:{}".format(port))
    await server.start()
    await server.wait_for_termination()


asyncio.run(serve())
