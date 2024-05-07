import orchestrator_pb2 as pb2
import orchestrator_pb2_grpc as grpc_pb2


import grpc.aio as agrpc
import grpc

import asyncio

task_channel_port = 8070
model_handler_port = 8071
model_port = 8072

task_channel = grpc.insecure_channel(f"localhost:{task_channel_port}")
model_channel = grpc.insecure_channel(f"localhost:{model_port}")
model_handler_channel = grpc.insecure_channel(f"localhost:{model_handler_port}")

task_stub = grpc_pb2.taskServiceStub(task_channel)
model_stub = grpc_pb2.ModelStub(model_channel)
model_handler_stub = grpc_pb2.ModelHandlerStub(model_handler_channel)

task_receivers = {}
model_receivers = {}
model_handler_receivers = {}


def start_model_handling():
    # Register the model
    model_request = pb2.Empty()
    modelDef = model_stub.registerModel(model_request)
    done = model_handler_stub.registerModel(modelDef)


async def start_task(stub):
    task_request = pb2.Empty()
    tasks = stub.startTask(task_request)
    async for task in tasks:
        print("Starting task with")
        print(task)
        model_handler_stub.startTask(task)


async def run_Task(stub):
    task_request = pb2.Empty()
    taskRequests = stub.runTask(task_request)
    async for taskRequest in taskRequests:
        print("Running task with")
        print(taskRequest)
        model_request = model_handler_stub.sendToModel(taskRequest)
        print("Sending to model")
        print(model_request)
        model_stub.predict(model_request)


async def finish_task(stub):
    task_request = pb2.Empty()
    finishTasks = stub.finishTask(task_request)
    async for finishRequest in finishTasks:
        print("Finishing task with:")
        print(finishRequest)
        metrics = model_handler_stub.finishTask(finishRequest)
        model_stub.publishMetrics(metrics)


async def returnPrediction(stub):
    print("Looping over prediction returns")
    model_request = pb2.Empty()
    print("Initializing Model")
    model_predictions = stub.sendPrediction(model_request)
    async for prediction in model_predictions:
        print("Returning prediction:")
        print(prediction)
        prediction = model_handler_stub.returnToTask(prediction)
        task_stub.getModelResponse(prediction)
    print("Finished looping")


start_model_handling()

print(task_receivers)


async def main():
    async_task_channel = agrpc.insecure_channel(f"localhost:{task_channel_port}")
    async_model_channel = agrpc.insecure_channel(f"localhost:{model_port}")

    async_task_stub = grpc_pb2.taskServiceStub(async_task_channel)
    async_model_stub = grpc_pb2.ModelStub(async_model_channel)
    await asyncio.gather(
        start_task(async_task_stub),
        run_Task(async_task_stub),
        finish_task(async_task_stub),
        returnPrediction(async_model_stub),
    )


asyncio.run(main())
