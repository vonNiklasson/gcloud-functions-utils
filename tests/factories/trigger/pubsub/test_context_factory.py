from datetime import datetime

import pytest

from tests.utils import is_base64_encoded, is_byte_encoded

from gcloud_functions_utils.factories.trigger.pubsub import ContextFactory, ContextMock, ContextEventType


def test_context_factory_build():
    context = ContextFactory.build()
    assert isinstance(context, ContextMock)


def test_field_types():
    context = ContextFactory.build()
    assert type(context.event_id) == str
    assert type(context.timestamp) == str
    assert type(context.event_type) == str
    assert type(context.resource) == str


def test_field_names():
    context = ContextFactory.build()
    assert isinstance(context, ContextMock)
    assert hasattr(context, 'event_id')
    assert hasattr(context, 'timestamp')
    assert hasattr(context, 'event_type')
    assert hasattr(context, 'resource')


def test_valid_event_type():
    event_type = 'google.pubsub.topic.publish'
    context = ContextFactory.build(event_type=ContextEventType.PubSubTopicPublish)
    assert context.event_type == event_type


def test_valid_event_type_from_string():
    event_type = 'google.pubsub.topic.publish'
    context = ContextFactory.build(event_type=event_type)
    assert context.event_type == event_type


def test_invalid_event_type_raises_exception():
    with pytest.raises(Exception):
        ContextFactory.build(event_type='invalid-event-type')
