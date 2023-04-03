import os
import threading

import openai
from dotenv import load_dotenv
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from module.chat_stream_handler import ChatStreamHandler
from module.threaded_generator import ThreadedGenerator

SYSTEM_PROMPT_TEXT = "あなたは日本人の一流ラッパーを演じてください。"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def stdout_streaming_sample():
    chat = ChatOpenAI(
        temperature=0.2,
        streaming=True,
        callback_manager=CallbackManager(
            handlers=[StreamingStdOutCallbackHandler()]
        ),
        verbose=True,
    )

    res = chat(
        [
            SystemMessage(content=SYSTEM_PROMPT_TEXT),
            HumanMessage(content="AI時代を危惧したラップを披露してください。"),
        ]
    )


def chat_worker(gen: ThreadedGenerator):
    try:
        chat = ChatOpenAI(
            temperature=0.2,
            streaming=True,
            callback_manager=CallbackManager(
                handlers=[StreamingStdOutCallbackHandler()]
            ),
            verbose=True,
        )
        chat(
            [
                SystemMessage(content=SYSTEM_PROMPT_TEXT),
                HumanMessage(content="AI時代を危惧したラップを披露してください。"),
            ]
        )
    except Exception as e:
        print(e)
    finally:
        gen.close()


def stream_chat() -> ThreadedGenerator:
    gen = ThreadedGenerator()
    threading.Thread(target=chat_worker, args=(gen)).start()
    return gen


if __name__ == "__main__":
    # stdout_streaming_sample()
    stream_chat()
