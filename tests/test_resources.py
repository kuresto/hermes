from datetime import datetime
from uuid import uuid4

import pytest

from hamcrest import assert_that, has_entries, has_key

from hermes.models import MessageQueue, MessageStatus


@pytest.fixture(name="message")
def fixture_message(client):
    now = datetime.utcnow()

    data = {
        "type": "sms",
        "scheduled_to": now.isoformat(),
        "sender": "+16981782417",
        "recipient": "+16981782417",
        "content": "ARGH",
        "params": [{"key": "param", "value": "content"}],
    }

    response = client.post("/messages/", json=data)

    assert response.status_code == 201
    return response.json()


def test_healthcheck(client):
    response = client.get("/healthcheck")

    assert response.status_code == 200
    assert_that(response.json(), has_entries({"health": True}))


def test_resource_add_message_to_queue(client):
    now = datetime.utcnow()

    data = {
        "type": "sms",
        "scheduled_to": now.isoformat(),
        "sender": "+16981782417",
        "recipient": "+16981782417",
        "content": "ARGH",
        "params": [{"key": "param", "value": "content"}],
    }

    response = client.post("/messages/", json=data)

    assert response.status_code == 201
    response_json = response.json()
    assert_that(
        response_json,
        has_entries(
            {
                "type": "sms",
                "scheduled_to": now.isoformat(),
                "sender": "+16981782417",
                "recipient": "+16981782417",
                "content": "ARGH",
                "status": "start",
                "status_message": None,
            }
        ),
        has_key("uuid"),
    )

    params = response_json["params"]

    assert_that(params[0], has_entries({"key": "param", "value": "content"}))


def test_resource_add_message_to_queue_without_params(client):
    now = datetime.utcnow()

    data = {
        "type": "sms",
        "scheduled_to": now.isoformat(),
        "sender": "+16981782417",
        "recipient": "+16981782417",
        "content": "ARGH",
    }

    response = client.post("/messages/", json=data)

    assert response.status_code == 201
    response_json = response.json()
    assert_that(
        response_json,
        has_entries(
            {
                "type": "sms",
                "scheduled_to": now.isoformat(),
                "sender": "+16981782417",
                "recipient": "+16981782417",
                "content": "ARGH",
                "status": "start",
                "status_message": None,
            }
        ),
        has_key("uuid"),
    )

    assert response_json["params"] == []


@pytest.mark.freeze_time("2017-05-21")
def test_resource_add_message_to_queue_to_the_past(client):
    data = {
        "type": "sms",
        "scheduled_to": datetime.utcnow().isoformat(),
        "sender": "+16981782417",
        "recipient": "+16981782417",
        "content": "ARGH",
    }

    response = client.post("/messages/", json=data)

    assert response.status_code == 422

    response_json = response.json()
    first_error = response_json["detail"][0]
    assert_that(
        first_error,
        has_entries(
            {
                "loc": ["body", "scheduled_to"],
                "msg": "You can only schedule a message now or for the future",
                "type": "assertion_error",
            }
        ),
    )


def test_resource_get_message(client, message):
    response = client.get(f"/messages/{message['uuid']}")

    assert response.status_code == 200
    assert_that(response.json(), has_entries(message))


def test_resource_get_message_not_found(client):
    uuid = str(uuid4())

    response = client.get(f"/messages/{uuid}")

    assert response.status_code == 404
    assert_that(response.json(), has_entries({"detail": f"Message {uuid} not found."}))


def test_resource_delete_message(client, message):
    response = client.delete(f"/messages/{message['uuid']}")

    assert response.status_code == 204
    assert_that(response.json(), has_entries({}))


def test_resource_delete_message_after_being_sent(client, message):
    message_instance = MessageQueue.query.filter(
        MessageQueue.uuid == message["uuid"]
    ).one()

    message_instance.set_status(MessageStatus.success)

    response = client.delete(f"/messages/{message['uuid']}")

    assert response.status_code == 400
    assert_that(
        response.json(),
        has_entries(
            {"detail": "You can't remove a message that was succesfully sent."}
        ),
    )
