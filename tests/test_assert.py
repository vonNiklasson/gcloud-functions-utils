import base64
import os

from gcloud_functions_utils.test_tools.clients.pubsub import PubSubClient
from tests.functions.dummy_function import dummy_function


def test_invoke():
    with PubSubClient(dummy_function) as client:
        response = client.publish('test')
        assert response.status_code == 200
