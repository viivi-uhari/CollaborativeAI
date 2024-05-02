import grpc.aio as grpc
from concurrent import futures
import asyncio
import random

# import the generated classes :
import model_handler_pb2
import model_handler_pb2_grpc

port = 8061

class ModelHandler(model_handler_pb2_grpc.CollaborateServicer):
  def __init__(self):
    self.model_list = []

  def startTask(self, request, context):
    suitable_models_list = []

    #Scan in the model list for the suitable model
    for model in self.model_list:
      if (request.need_text == model.can_text and request.need_image == model.can_image):
        suitable_models_list.append(model)

    #choose a random model if there are multiple that sastisfy the requirements
    chosen_model = random.choice(suitable_models_list)

    #assign the modelID to the session
    request.session["modelID"] = chosen_model.modelID

    return model_handler_pb2.Empty()

  def finishTask(self, request, context):
    taskMetrics = request.taskMetrics

    return model_handler_pb2.metricsJson()
  
  def sendToModel(self, request, context):
      
    return
  
  def returnToTask(self, request, context):
      
    return
  
  def registerModel(self, request, context):
    #add the models to the model list on startup
    self.model_list.append(request)
    return model_handler_pb2.Empty();

async def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  model_handler_pb2_grpc.add_ModelHandlerServicer_to_server(ModelHandler(), server)
  print("Starting the model handler server. Listening on port : " + str(port))
  server.add_insecure_port("0.0.0.0:{}".format(port))
  await server.start()
  await server.wait_for_termination()

asyncio.run(serve())
