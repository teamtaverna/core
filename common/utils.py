from time import time

LAST_TIMESTAMP = 0


def timestamp_seconds():
    global LAST_TIMESTAMP

    timestamp = int(time())
    LAST_TIMESTAMP = (LAST_TIMESTAMP + 1) if timestamp <= LAST_TIMESTAMP else timestamp

    return LAST_TIMESTAMP
