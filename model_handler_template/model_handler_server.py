import grpc
import model_handler_pb2
import model_handler_pb2_grpc


from concurrent import futures

port = 8061

# class ModelHandler(model_handler_pb2_grpc.CollaborateServicer):

    
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
model_handler_pb2_grpc.add_ModelHandlerServicer_to_server(ModelHandler(), server)
server.add_insecure_port("0.0.0.0:{}".format(port))
server.start()