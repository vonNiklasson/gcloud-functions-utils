from gcloud_functions_utils.factories.trigger.pubsub import EventFactory
from gcloud_functions_utils.parsers.trigger.pubsub import EventParser


def test_parse_empty_event():
    EventParser({})


def test_parse_from_factory():
    event = EventFactory.build()
    parsed_event = EventParser(event)


def test_parsed_factory_decodes_data():
    original_message = "Hello there!"
    event = EventFactory.build(data="Hello there!")
    parsed_event = EventParser(event)
    assert parsed_event.data == original_message
