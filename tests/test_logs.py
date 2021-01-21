# pylint: disable=anomalous-backslash-in-string,line-too-long
import re
from io import StringIO
from logging import INFO, Formatter, StreamHandler

import pytest

from hermes.logs import get_logger


@pytest.fixture(name="logger_regex", scope="module")
def fixture_logger_regex():
    regex_str = r"\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\]\s\[[A-z]+\]\s\[[A-z._]+\]\s.+"

    return re.compile(regex_str)


@pytest.mark.parametrize(
    "command, message",
    [
        ("info", "fake log, info message"),
        ("warning", "fake log, warning message"),
        ("error", "fake log, error message"),
        ("critical", "fake log, critical message"),
    ],
)
def test_log_success(logger_regex, command, message):
    logger = get_logger(__name__)

    # Adding log stream to IO to capture it's output
    log_stream = StringIO()
    handler = StreamHandler(log_stream)
    handler.setLevel(INFO)
    formatter = Formatter(logger.handlers[0].formatter._fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    log_func = getattr(logger, command)
    log_func(message)
    log_result = log_stream.getvalue().split("\n")[0]

    assert logger_regex.match(log_result)
