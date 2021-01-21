import sys
from logging import Formatter, StreamHandler, Logger, INFO


def get_logger(name):
    formatter = Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")

    handler = StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(INFO)

    logger = Logger(name)
    logger.setLevel(INFO)
    logger.addHandler(handler)

    return logger
