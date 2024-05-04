import time


def elapsed_time(given_time) -> float:
    return now() - given_time


def now() -> float:
    return time.time()
