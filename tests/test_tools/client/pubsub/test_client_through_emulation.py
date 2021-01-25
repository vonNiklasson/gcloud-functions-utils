import base64

import pytest
from tests.functions import pubsub
from tests.utils import is_base64_encoded, is_byte_encoded

from gcloud_functions_utils.test_tools.local_client.pubsub import LocalPubSubClient


@pytest.mark.emulation
def test_emulated_pubsub():
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish("")
        assert response.status_code == 200


@pytest.mark.emulation
def test_event_payload_has_data():
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish("")
        assert response.status_code == 200
        output = client.get_json()
        assert "data" in output


@pytest.mark.emulation
def test_event_data_is_base64_encoded():
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish("")
        assert response.status_code == 200
        output = client.get_json()
        assert is_base64_encoded(output["data"])


@pytest.mark.emulation
def test_event_data_byte_encoded():
    original_message = "Hello there!"
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_json()
        data_message = base64.b64decode(output["data"])
        assert is_byte_encoded(data_message)


@pytest.mark.emulation
def test_event_data_is_preserved():
    original_message = "Hello there!"
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_json()
        data_message = base64.b64decode(output["data"]).decode("utf-8")
        assert data_message == original_message


@pytest.mark.emulation
def test_event_attributes_is_transferred():
    attributes = {"Hello": "there!"}
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish("", attributes=attributes)
        assert response.status_code == 200
        output = client.get_json()
        assert "attributes" in output
        assert output["attributes"] is not None


@pytest.mark.emulation
def test_event_attributes_are_preserved():
    attributes = {
        "Hello": "there!",
        "General": "Kenobi",
    }
    with LocalPubSubClient(pubsub.basic_print_event) as client:
        response = client.publish("", attributes=attributes)
        assert response.status_code == 200
        output = client.get_json()

        assert len(output["attributes"].keys()) == len(attributes.keys())
        assert output["attributes"]["Hello"] == "there!"
        assert output["attributes"]["General"] == "Kenobi"
