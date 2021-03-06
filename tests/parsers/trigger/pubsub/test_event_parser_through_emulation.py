import pytest
from tests.functions import pubsub
from tests.utils import is_base64_encoded

from gcloud_functions_utils.test_tools.local_client.pubsub import LocalPubSubClient


@pytest.mark.emulation
def test_parser_event_data_is_not_base64_encoded():
    original_message = "Hello there!"
    with LocalPubSubClient(pubsub.parser_print_event_data) as client:
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_output()
        assert not is_base64_encoded(output)


@pytest.mark.emulation
def test_parser_decodes_data():
    original_message = "Hello there!"
    with LocalPubSubClient(pubsub.parser_print_event_data) as client:
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_output()
        assert output == original_message


@pytest.mark.emulation
def test_parser_attributes_are_preserved():
    attributes = {
        "Hello": "there!",
        "General": "Kenobi",
    }
    with LocalPubSubClient(pubsub.parser_print_event_attributes) as client:
        response = client.publish("", attributes=attributes)
        assert response.status_code == 200
        output = client.get_json()

        assert len(output.keys()) == len(attributes.keys())
        assert output["Hello"] == "there!"
        assert output["General"] == "Kenobi"
