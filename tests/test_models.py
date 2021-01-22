from datetime import datetime
import pytest

from hamcrest import has_entries, assert_that

from hermes.models import MessageQueue, MessageQueueHistory, MessageStatus, MessageType


def test_message_queue_create(mixer):
    message = mixer.blend("hermes.models.MessageQueue", type=MessageType.sms)

    assert message.status == MessageStatus.start


def test_message_queue_fetch(session, mixer):
    mixer.blend("hermes.models.MessageQueue", type=MessageType.sms)

    message = session.query(MessageQueue).one()
    assert message.status == MessageStatus.start


def test_message_queue_listing(session, mixer):
    mixer.cycle(5).blend("hermes.models.MessageQueue", type=MessageType.sms)

    messages = session.query(MessageQueue).all()

    assert len(messages) == 5


def test_message_queue_update(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue", type=MessageType.sms)

    assert message.status == MessageStatus.start

    message.status = MessageStatus.processing
    session.commit()

    session.refresh(message)
    assert message.status == MessageStatus.processing


def test_message_queue_update_invalid_status(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue", type=MessageType.sms)

    assert message.status == MessageStatus.start

    with pytest.raises(ValueError):
        message.status = "invalid"
        session.commit()


def test_message_queue_delete(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue", type=MessageType.sms)

    assert session.query(MessageQueue).count() == 1

    session.query(MessageQueue).filter(MessageQueue.uuid == message.uuid).delete()
    session.commit()

    assert session.query(MessageQueue).count() == 0


def test_base_queue_create():
    # Should be able to add an entry to queue history automatically.
    now = datetime.now()

    message = MessageQueue.create(
        **{
            "type": MessageType.sms,
            "scheduled_to": now,
            "sender": "myself",
            "recipient": "fake",
            "content": "fake-content",
            "status_message": "fake-start",
        }
    )

    assert_that(
        message.__dict__,
        has_entries(
            {
                "type": MessageType.sms,
                "uuid": message.uuid,
                "scheduled_to": now,
                "sender": "myself",
                "recipient": "fake",
                "content": "fake-content",
                "status": MessageStatus.start,
                "status_message": "fake-start",
            }
        ),
    )
    assert message.created and message.updated

    assert len(message.history) == 1

    history = message.history[0]

    assert_that(
        history.__dict__,
        has_entries(
            {
                "type": MessageType.sms,
                "message_uuid": message.uuid,
                "scheduled_to": now,
                "sender": "myself",
                "recipient": "fake",
                "content": "fake-content",
                "status": MessageStatus.start,
                "status_message": "fake-start",
            }
        ),
    )


def test_base_queue_update(session):
    now = datetime.now()

    message = MessageQueue.create(
        **{
            "type": MessageType.sms,
            "scheduled_to": now,
            "sender": "myself",
            "recipient": "fake",
            "content": "fake-content",
            "status_message": "fake-start",
        }
    )

    assert message.status == MessageStatus.start

    assert len(message.history) == 1

    message.update(**{"status": MessageStatus.in_flight})

    assert message.status == MessageStatus.in_flight

    session.expire(message)
    assert len(message.history) == 2


def test_base_queue_delete(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue", type=MessageType.sms)
    message_uuid = message.uuid

    assert session.query(MessageQueue).count() == 1

    message.delete()

    assert not MessageQueue.exists(MessageQueue.uuid == message_uuid)
    assert session.query(MessageQueueHistory).count() == 0
