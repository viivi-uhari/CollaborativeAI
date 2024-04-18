from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers.task_router import router as task_router
from routers.chat import router as chat_router
from routers.session import router as session_router

from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
origins = ["http://localhost", "http:/localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)


app.include_router(task_router)
app.include_router(chat_router)
app.include_router(session_router)

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
