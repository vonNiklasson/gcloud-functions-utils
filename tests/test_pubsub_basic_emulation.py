import base64
from gcloud_functions_utils.test_tools.clients.pubsub import PubSubClient
from tests.functions import pubsub
from tests.utils import is_byte_encoded, is_base64_encoded


def test_emulated_pubsub():
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish('')
        assert response.status_code == 200


def test_event_payload_has_data():
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish('')
        assert response.status_code == 200
        output = client.get_json()
        assert 'data' in output


def test_event_data_is_base64_encoded():
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish('')
        assert response.status_code == 200
        output = client.get_json()
        assert is_base64_encoded(output['data'])


def test_event_data_byte_encoded():
    original_message = "Hello there!"
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_json()
        data_message = base64.b64decode(output['data'])
        assert is_byte_encoded(data_message)


def test_event_data_is_preserved():
    original_message = "Hello there!"
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_json()
        data_message = base64.b64decode(output['data']).decode('utf-8')
        assert data_message == original_message


def test_event_attributes_is_transferred():
    attributes = {'Hello': 'there!'}
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish('', attributes=attributes)
        assert response.status_code == 200
        output = client.get_json()
        assert 'attributes' in output
        assert output['attributes'] is not None


def test_event_attributes_are_preserved():
    attributes = {
        'Hello': 'there!',
        'General': 'Kenobi',
    }
    with PubSubClient(pubsub.basic_print_event) as client:
        response = client.publish('', attributes=attributes)
        assert response.status_code == 200
        output = client.get_json()

        assert len(output['attributes'].keys()) == len(attributes.keys())
        assert output['attributes']['Hello'] == 'there!'
        assert output['attributes']['General'] == 'Kenobi'
