import queue


class ThreadedGenerator:
    def __init__(self) -> None:
        self.queue = queue.Queue()

    def __iter__(self) -> None:
        return self

    def __next__(self) -> None:
        item = self.queue.get()
        if item is StopIteration:
            raise StopIteration
        else:
            return item

    def send(self, value: str) -> None:
        self.queue.put(value)

    def close(self) -> None:
        self.queue.put(StopIteration)
