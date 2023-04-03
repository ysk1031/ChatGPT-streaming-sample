from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from server.python.threaded_generator import ThreadedGenerator


class ChatStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen: ThreadedGenerator) -> None:
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.gen.put(token)
