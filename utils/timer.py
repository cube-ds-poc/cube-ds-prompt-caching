import time

class Timer:
    def __init__(self, label: str):
        self.label = label
        self.start = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        end = time.perf_counter()
        print(f"[TIMER] {self.label}: {end - self.start:.3f} sec")
