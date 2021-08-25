import time


class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self._timer = time.perf_counter()

    def count(self):
        current = time.perf_counter()
        return current - self._timer
