from hamcrest import assert_that, has_entries


def test_healthcheck(client):
    response = client.get("/healthcheck")

    assert response.status_code == 200
    assert_that(response.json(), has_entries({"health": True}))


def test_resource_add_message_to_queue():
    pass


def test_resource_get_message():
    pass


def test_resource_delete_message():
    pass


def test_resource_delete_message_after_being_sent():
    pass


def test_resource_update_message():
    pass


def test_resource_update_message_after_being_sent():
    pass
