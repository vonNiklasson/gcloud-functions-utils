import base64
import inspect
import os
import subprocess
import uuid
from typing import Callable

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class PubSubPublisher:
    def __init__(self, url: str, session: Session):
        self.url = url
        self.session = session

    def publish(self, data):
        encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        pubsub_message = {"data": {"data": encoded_data}}

        return self.session.post(self.url, json=pubsub_message)


class PubSubClient:
    def __init__(self, func: Callable, port: int = 8888):
        self.func = func
        self.name = str(uuid.uuid4())
        self.port = port
        self.url = f"http://localhost:{self.port}/"
        self.retry_adapter = HTTPAdapter(max_retries=Retry(total=6, backoff_factor=1))

        self.target = self.func.__name__
        self.source = inspect.getfile(self.func)

    def __enter__(self):
        self.session = requests.Session()
        self.session.mount(self.url, self.retry_adapter)

        self.process = subprocess.Popen(
            [
                "functions-framework",
                "--target",
                self.target,
                "--source",
                self.source,
                "--signature-type",
                "event",
                "--port",
                str(self.port),
            ],
            cwd=os.path.dirname(__file__),
            stdout=None,
        )

        return PubSubPublisher(self.url, self.session)

    def __exit__(self, exception_type, exception_value, traceback):
        self.process.kill()
        if self.process.stdout:
            self.process.stdout.close()
        if self.process.stderr:
            self.process.stderr.close()
        if self.process.stdin:
            self.process.stdin.close()
        # Wait for the process to terminate, to avoid zombies.
        self.process.wait()
