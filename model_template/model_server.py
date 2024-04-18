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

port = 8061

model_definition = model_pb2.modelDefinition()
model_definition.needs_text = True
model_definition.needs_image = False
model_definition.can_text = True
model_definition.can_image = False
model_definition.modelID = "GPT4_turbo"


# create a class to define the server functions, derived from
class ModelServicer(model_pb2_grpc.ModelServicer):
    def publishMetrics(self, request, context):
        if model_definition.modelID != request.modelID:
            context.abort(StatusCode.UNIMPLEMENTED, "You've reached the wrong service.")
            return
        # define the buffer of the response :
        response = model_pb2.modelAnswer()
        # get the value of the response by calling the desired function :
        response.answer = str(ai_model.publish_metrics(request.metrics))
        return response

    async def predict(self, request, context):
        # define the buffer of the response :
        response = model_pb2.modelAnswer()
        # get the value of the response by calling the desired function :
        response.answer = (await ai_model.get_response(request)).model_dump_json()
        return response

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
