import base64
from datetime import datetime

from tests.utils import is_base64_encoded, is_byte_encoded

from gcloud_functions_utils.factories.trigger.pubsub import EventFactory


def test_event_factory_build():
    event = EventFactory.build()
    assert type(event) == dict


def test_field_types():
    event = EventFactory.build(
        data="Hello there!", attributes={}, message_id=1, publish_time=datetime.utcnow(), ordering_key="2"
    )
    assert type(event["data"]) == bytes
    assert type(event["attributes"]) == dict
    assert type(event["messageId"]) == str
    assert type(event["publishTime"]) == str
    assert type(event["orderingKey"]) == str


def test_field_names():
    event = EventFactory.build(
        data="Hello there!", attributes={}, message_id=1, publish_time=datetime.utcnow(), ordering_key="2"
    )
    assert "data" in event
    assert "attributes" in event
    assert "messageId" in event
    assert "publishTime" in event
    assert "orderingKey" in event


def test_data_is_byte_encoded():
    original_message = "Hello there!"
    event = EventFactory.build(data=original_message)
    assert is_byte_encoded(event["data"])


def test_data_is_base64_encoded():
    original_message = "Hello there!"
    event = EventFactory.build(data=original_message)
    byte_decoded = event["data"].decode("utf-8")
    assert is_base64_encoded(byte_decoded)


def test_data_is_preserved():
    original_message = "Hello there!"
    event = EventFactory.build(data=original_message)
    byte_decoded = event["data"].decode("utf-8")
    base64_decoded = base64.b64decode(byte_decoded).decode("utf-8")
    assert base64_decoded == original_message
