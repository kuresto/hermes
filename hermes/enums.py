from enum import Enum


class MessageStatus(Enum):
    start = "start"
    in_flight = "in_flight"
    processing = "processing"
    success = "success"
    error = "error"
    dead = "dead"
