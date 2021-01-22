import pytest

from mixer.backend.sqlalchemy import Mixer

from fastapi.testclient import TestClient

from hermes.app import app
from hermes.db import session
from hermes.models import *


@pytest.fixture(name="client")
def fixture_client():
    return TestClient(app)


@pytest.fixture(name="mixer", scope="function")
def fixture_mixer():
    return Mixer(session=session, commit=True)


@pytest.fixture(name="session", scope="function")
def fixture_session():
    yield session

    session.rollback()


@pytest.fixture(autouse=True, name="db_init")
def fixture_database_init():
    BaseModel.metadata.create_all()

    yield

    BaseModel.metadata.drop_all()
