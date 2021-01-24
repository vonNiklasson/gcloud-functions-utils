import base64
import binascii


def is_byte_encoded(string):
    try:
        string.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def is_base64_encoded(string):
    try:
        base64.b64decode(string)
    except binascii.Error:
        return False
    return True
