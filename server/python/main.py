import os

import openai
from dotenv import load_dotenv
from langchain.callbacks.base import CallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from server.python.chat_stream_handler import ChatStreamHandler
from server.python.threaded_generator import ThreadedGenerator

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def streaming_sample():
    chat = ChatOpenAI(
        temperature=0.2,
        streaming=True,
        callback_manager=CallbackManager(
            handlers=[ChatStreamHandler(gen=ThreadedGenerator())]
        ),
        verbose=True,
    )

    res = chat(
        [
            SystemMessage(content="あなたは日本人の一流ラッパーを演じてください。。"),
            HumanMessage(content="AI時代を危惧したラップを披露してください。"),
        ]
    )


if __name__ == "__main__":
    streaming_sample()
