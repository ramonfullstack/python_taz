import base64
import json


def parse_base64_to_dict(content):
    return json.loads(str(base64.b64decode(content), encoding='utf-8'))
