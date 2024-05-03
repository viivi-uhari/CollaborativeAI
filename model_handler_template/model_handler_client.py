import logging

import grpc
import model_handler_pb2
import model_handler_pb2_grpc


def run():
    print("calling Model Handler stub...")
    with grpc.insecure_channel("localhost:8061") as channel:
        stub = model_handler_pb2_grpc.ModelHandlerStub(channel)
        stub.startTask(model_handler_pb2.modelRequirements(
                needs_text=True,
                needs_image=True,
                sessionID="123456789"
            )
        )
        response = stub.finishTask(model_handler_pb2.taskMetrics(
                metrics="test metrics",
                sessionID="123456789"
            )
        )
        print("After calling the finishTask endpoint, model Handler client received: ")
        print(response)

if __name__ == "__main__":
    logging.basicConfig()
    run()