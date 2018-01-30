import json


def build_json_response(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)
