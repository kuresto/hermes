import pytest

from fastapi.testclient import TestClient

from hermes.app import app


@pytest.fixture(name="client")
def fixture_client():
    return TestClient(app)
