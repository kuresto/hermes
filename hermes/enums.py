from enum import Enum


class MessageStatus(str, Enum):
    start = "start"
    in_flight = "in_flight"
    processing = "processing"
    success = "success"
    error = "error"
    dead = "dead"


class MessageType(Enum):
    email = "email"
    sms = "sms"
    push = "push"
    whatsapp = "whatsapp"
