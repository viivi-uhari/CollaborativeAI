from fastapi import FastAPI, Request
import logging
from routers.task_router import task_router, task_handler
from routers.session import router as session_router
from grpc_server import task_server


# This will need to be adapted by the individual task!
from tasks.tangram import Tangram

tangram_task = Tangram()
task_handler.set_Task(tangram_task)

# Router handling.
app = FastAPI()

app.include_router(task_router)
app.include_router(session_router)

# This logging middleware is mainly for debugging purposes.
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    log_message = f"Received request: {method} {path}"
    logging.info(log_message)
    logging.info(request.headers)
    response = await call_next(request)
    return response


# Start the GRPC Server
import grpc
from concurrent import futures

import grpc_server.tasks_pb2_grpc as task_pb2_grpc
import grpc_server.task_server as task_server
from grpc_server.queue_handler import queue_handler

port = 8061

# create a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
task_pb2_grpc.add_taskServiceServicer_to_server(
    task_server.TaskServicer(queue_handler), server
)
print("Starting GRPC server. Listening on port : " + str(port))
server.add_insecure_port("0.0.0.0:{}".format(port))
server.start()
