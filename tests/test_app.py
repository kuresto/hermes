from subprocess import Popen, PIPE

from hermes.logs import get_logger


logger = get_logger(__name__)


def test_app_init():
    assert True


def test_app_requirements_safety():
    p = Popen(
        ["safety", "check", "-r", "requirements/development.txt"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    output, _ = p.communicate()
    rc_development = p.returncode  # If 0 has no vulnerable packages, if 255, it has.

    logger.info("\n==== Development:\n%s", output.decode())

    assert rc_development != 255

    p = Popen(
        ["safety", "check", "-r", "requirements/production.txt"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    output, _ = p.communicate()
    rc_production = p.returncode  # If 0 has no vulnerable packages, if 255, it has.

    logger.info("\n==== Production:\n%s", output.decode())

    assert rc_production != 255
