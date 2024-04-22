from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers.task_router import router as task_router
from routers.session import router as session_router

app = FastAPI()

app.include_router(task_router)
app.include_router(session_router)

origins = ["http://localhost", "http:/localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


import grpc
from concurrent import futures

# import the generated classes :
import gprc_server.tasks_pb2_grpc as task_pb2_grpc
import gprc_server.task_server as task_server
from gprc_server.queue_handler import queue_handler

# import the function we made :


port = 8061

# create a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
task_pb2_grpc.add_taskServiceServicer_to_server(
    task_server.TaskServicer(queue_handler), server
)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("0.0.0.0:{}".format(port))
server.start()
