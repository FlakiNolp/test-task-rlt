import json


def filter_dict(text: str):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False
