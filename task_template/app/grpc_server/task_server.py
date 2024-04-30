import grpc_server.tasks_pb2_grpc as tasks_pb2_grpc
import grpc_server.tasks_pb2 as tasks_pb2
import queue
import logging
import traceback
import grpc_server.queue_handler as queue_handler
import asyncio

required_properties = tasks_pb2.modelRequirements()
required_properties.needs_text = True
required_properties.needs_image = False


def get_required_props():
    required_properties = tasks_pb2.modelRequirements()
    required_properties.needs_text = True
    required_properties.needs_image = False
    return required_properties


class TaskServicer(tasks_pb2_grpc.taskServiceServicer):
    def __init__(
        self,
        queue_handler: queue_handler.QueueHandler,
    ):
        self.queue_handler = queue_handler

    async def startTask(self, request, context):
        _ = request
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                try:
                    session = self.queue_handler.start_queue.get(timeout=1.0)
                    job = get_required_props()
                    job.sessionID = session

                except queue.Empty:
                    # leave if orchestrator disconnected
                    if not context.is_active():
                        logging.info("RPC inactive - leaving startTask")
                        break
                    # Sleep a bit and let other parts continue
                    await asyncio.sleep(1)
                else:
                    # Init the response queue, and yield the job, to have the model handler work properly.
                    self.queue_handler.response_queues[job.sessionID] = queue.Queue()
                    yield job

            except Exception as e:
                logging.info(
                    "exception in startTask: %s\n%s", e, traceback.format_exc()
                )
                # allow new call to start
                break

    async def runTask(self, request, context):
        _ = request
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                try:
                    data = self.queue_handler.task_queue.get(timeout=1.0)
                    job = tasks_pb2.taskRequest()
                    job.sessionID = data["sessionID"]
                    job.request = data["request"]
                except queue.Empty:
                    # leave if orchestrator disconnected
                    if not context.is_active():
                        logging.info("RPC inactive - leaving runTask")
                        break
                    await asyncio.sleep(1)
                else:
                    yield job

            except Exception as e:
                logging.info("exception in runTask: %s\n%s", e, traceback.format_exc())
                # allow new call to start
                break

    async def finishTask(self, request, context):
        # get the value of the response by calling the desired function :
        _ = request
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                try:
                    data = self.queue_handler.finish_queue.get(timeout=1.0)
                    job = tasks_pb2.taskMetrics()
                    job.sessionID = data.session
                    job.metrics = data.metrics
                except queue.Empty:
                    # leave if orchestrator disconnected
                    if not context.is_active():
                        logging.info("RPC inactive - leaving finishTask")
                        break
                    await asyncio.sleep(1)
                else:
                    yield job

            except Exception as e:
                logging.info(
                    "exception in finishTask: %s\n%s", e, traceback.format_exc()
                )
                # allow new call to start
                break

    def getModelResponse(self, request, context):
        if request.sessionID in self.queue_handler.response_queues:
            current_queue = self.queue_handler.response_queues[request.sessionID]
            current_queue.put(request.answer)
        else:
            logging.error(
                "Session ID not found in response_queues, couldn't hanlde request"
            )
        return tasks_pb2.Empty()
