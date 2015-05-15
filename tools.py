from flask import Response
from functools import wraps
import json

def is_int(string):
    try:
        int(string)
    except ValueError:
        return False
    return True

def to_json(dict, pretty=False):
    return json.dumps(dict) if not pretty else json.dumps(dict, indent=4, separators=(',', ': '))

def api_response(result, pretty=True):
    return Response(to_json(result, pretty=pretty), mimetype="application/json")

def response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return api_response(func(*args, **kwargs))
    return wrapper