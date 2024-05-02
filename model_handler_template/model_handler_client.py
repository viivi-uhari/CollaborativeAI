import logging

import grpc
import model_handler_pb2
import model_handler_pb2_grpc


def run():
    print("calling Model Handler stub...")
    with grpc.insecure_channel("localhost:8061") as channel:
        stub = model_handler_pb2_grpc.ModelHandlerStub(channel)
        #response = stub.startTask(model_handler_pb2.Response(response="Hello world"))
        response = stub.startTask(model_handler_pb2.modelRequirements(
                needs_text=True,
                needs_image=False,
                sessionID="test"
            )
        )
        print("Model Handler client received: " + response)

if __name__ == "__main__":
    logging.basicConfig()
    run()