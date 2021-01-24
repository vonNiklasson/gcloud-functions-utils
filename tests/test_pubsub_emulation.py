import base64
from gcloud_functions_utils.test_tools.clients.pubsub import PubSubClient
from tests.functions import dummy
from tests.utils import is_byte_encoded, is_base64_encoded


def test_emulated_pubsub():
    with PubSubClient(dummy.dummy_function, 8080) as client:
        response = client.publish('')
        assert response.status_code == 200


def test_event_payload_has_data():
    with PubSubClient(dummy.dummy_function, 8081) as client:
        response = client.publish('')
        assert response.status_code == 200
        output = client.get_json()
        assert 'data' in output


def test_event_data_is_base64_encoded():
    with PubSubClient(dummy.dummy_function, 8082) as client:
        response = client.publish('')
        assert response.status_code == 200
        output = client.get_json()
        assert is_base64_encoded(output['data'])


def test_event_data_byte_encoded():
    with PubSubClient(dummy.dummy_function, 8083) as client:
        original_message = "Hello there!"
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_json()
        data_message = base64.b64decode(output['data'])
        assert is_byte_encoded(data_message)


def test_event_data_is_preserved():
    with PubSubClient(dummy.dummy_function, 8084) as client:
        original_message = "Hello there!"
        response = client.publish(original_message)
        assert response.status_code == 200
        output = client.get_json()
        data_message = base64.b64decode(output['data']).decode('utf-8')
        assert data_message == original_message


def test_event_attributes_is_transferred():
    with PubSubClient(dummy.dummy_function, 8084) as client:
        response = client.publish('', attributes={'Hello': 'there!'})
        assert response.status_code == 200
        output = client.get_json()
        assert 'attributes' in output
        assert output['attributes'] is not None


def test_event_attributes_are_preserved():
    with PubSubClient(dummy.dummy_function, 8084) as client:
        attributes = {
            'Hello': 'there!',
            'General': 'Kenobi',
        }
        response = client.publish('', attributes=attributes)
        assert response.status_code == 200
        output = client.get_json()

        assert len(output['attributes'].keys()) == len(attributes.keys())
        assert output['attributes']['Hello'] == 'there!'
        assert output['attributes']['General'] == 'Kenobi'
