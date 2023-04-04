import os
import threading

import openai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from module.chat_stream_handler import ChatStreamHandler
from module.threaded_generator import ThreadedGenerator

SYSTEM_PROMPT_TEXT = """
あなたは日本人の一流ラッパーを演じてください。日本語でラップします。
"""

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

origins = [
    "http://localhost:3000",  # Next.jsからのアクセス用
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def stdout_streaming_sample() -> None:
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


def chat_worker(gen: ThreadedGenerator, prompt: str) -> None:
    try:
        chat = ChatOpenAI(
            temperature=0.2,
            streaming=True,
            callback_manager=CallbackManager(
                handlers=[ChatStreamHandler(gen=gen)]
            ),
            verbose=True,
        )
        chat(
            [
                SystemMessage(content=SYSTEM_PROMPT_TEXT),
                HumanMessage(content=prompt),
            ]
        )
    except Exception as e:
        print(e)
    finally:
        gen.close()


def stream_chat(prompt: str) -> ThreadedGenerator:
    gen = ThreadedGenerator()
    threading.Thread(target=chat_worker, args=(gen, prompt)).start()
    return gen


@app.post("/streaming_chat")
async def streaming():
    return StreamingResponse(
        stream_chat(prompt="AI時代を危惧したラップを披露してください。"),
        media_type="text/event-stream",
    )


def app_start():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    # stdout_streaming_sample()
    app_start()
