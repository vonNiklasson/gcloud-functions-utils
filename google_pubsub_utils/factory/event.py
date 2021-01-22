import base64
from datetime import datetime


class EventFactory:
    @staticmethod
    def create(data="", attributes=None, message_id=0, publish_time=None, ordering_key=""):
        if publish_time is None:
            publish_time = datetime.utcnow().isoformat("T") + "Z"

        event = {"data": base64.b64encode(data.encode("utf-8")), "messageId": message_id, "publishTime": publish_time}

        if attributes is not None:
            event["attributes"] = attributes

        if ordering_key is not None:
            event["orderingKey"] = ordering_key

        return event
