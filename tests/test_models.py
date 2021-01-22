import pytest

from hermes.models import MessageQueue, MessageStatus


def test_base_model_create(mixer):
    # Should be able to add an entry to queue history automatically.
    message = mixer.blend("hermes.models.MessageQueue")

    assert message.status == MessageStatus.start


def test_base_model_fetch(session, mixer):
    mixer.blend("hermes.models.MessageQueue")

    message = session.query(MessageQueue).one()
    assert message.status == MessageStatus.start


def test_base_model_listing(session, mixer):
    mixer.cycle(5).blend("hermes.models.MessageQueue")

    messages = session.query(MessageQueue).all()

    assert len(messages) == 5


def test_base_model_update(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue")

    assert message.status == MessageStatus.start

    message.status = MessageStatus.processing
    session.commit()

    session.refresh(message)
    assert message.status == MessageStatus.processing


def test_base_model_update_invalid_status(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue")

    assert message.status == MessageStatus.start

    with pytest.raises(ValueError):
        message.status = "invalid"
        session.commit()


def test_base_model_delete(session, mixer):
    message = mixer.blend("hermes.models.MessageQueue")

    assert session.query(MessageQueue).count() == 1

    session.query(MessageQueue).filter(MessageQueue.uuid == message.uuid).delete()
    session.commit()

    assert session.query(MessageQueue).count() == 0
