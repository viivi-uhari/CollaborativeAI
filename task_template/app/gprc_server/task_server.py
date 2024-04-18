import tasks_pb2_grpc
import tasks_pb2
import queue
import logging
import traceback
import queue_handler

required_properties = tasks_pb2.modelProps()
required_properties.needs_text = True
required_properties.needs_image = False


def get_required_props():
    required_properties = tasks_pb2.modelProps()
    required_properties.needs_text = True
    required_properties.needs_image = False
    return required_properties


class TaskServicer(tasks_pb2_grpc.taskServiceServicer):
    def __init__(
        self,
        queue_handler: queue_handler.QueueHandler,
    ):
        self.queue_handler = queue_handler

    def startTask(self, request, context):
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
                else:
                    yield job

            except Exception as e:
                logging.info(
                    "exception in startTask: %s\n%s", e, traceback.format_exc()
                )
                # allow new call to start
                break

    def runTask(self, request, context):
        _ = request
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                try:
                    data = self.queue_handler.task_queue.get(timeout=1.0)
                    job = tasks_pb2.taskRequest()
                    job.sessionID = data.session
                    job.request = data.request
                except queue.Empty:
                    # leave if orchestrator disconnected
                    if not context.is_active():
                        logging.info("RPC inactive - leaving runTask")
                        break
                else:
                    yield job

            except Exception as e:
                logging.info("exception in runTask: %s\n%s", e, traceback.format_exc())
                # allow new call to start
                break

    def finishTask(self, request, context):
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
