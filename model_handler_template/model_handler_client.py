import logging

import grpc
import model_handler_pb2
import model_handler_pb2_grpc


def run():
    print("calling Model Handler stub...")
    # with grpc.insecure_channel("localhost:8061") as channel:
    #     stub = model_handler_pb2_grpc.ModelHandlerStub(channel)
    #     response = 
    print("Model Handler client received: ")


if __name__ == "__main__":
    logging.basicConfig()
    run()