from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
import logging
from data_models import *

logger = logging.getLogger(__name__)

# NOTE: This needs to be defined in the environment this model is running in.
default_headers = {"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}


ChatOpenAI(
    base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/gpt4-1106-preview/",
    default_headers=default_headers,
)


def publish_metrics(metrics_json: str):
    logger.info(metrics_json)
    return True


async def get_response(message: TaskInput) -> TaskOutput:
    model = ChatOpenAI(
        base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/gpt4-1106-preview/",
        default_headers=default_headers,
    )

    history_template = ChatPromptTemplate.from_messages(
        [
            ("system", message.system),
            MessagesPlaceholder("chat_history"),
            ("human", {"input"}),
        ]
    )

    history = []
    if len(message.text) > 1:
        for i in range(len(message.text) - 1):
            inputMessage = message.text[i]
            if inputMessage.role == "user":
                history.append(HumanMessage(inputMessage.content))
            else:
                history.append(AIMessage(inputMessage.content))
    history_chain = create_stuff_documents_chain(model, history_template)
    AIresponse = await history_chain.invoke(
        input=message.text[-1], chat_history=history
    )
    taskResponse = TaskOutput()
    taskResponse.text = AIresponse.content
    return taskResponse
