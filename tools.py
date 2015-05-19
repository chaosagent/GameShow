from flask import Response, request
from functools import wraps
import json
from collections import OrderedDict

def is_int(string):
    try:
        int(string)
    except ValueError:
        return False
    return True

def to_json(dict, pretty=False):
    return json.dumps(dict) if not pretty else json.dumps(dict, indent=4, separators=(',', ': '))

def gen_api_response(result, pretty=True):
    return Response(to_json(result, pretty=pretty), mimetype="application/json")

def api_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return gen_api_response(func(*args, **kwargs))
    return wrapper

def requires_args(required_args=()):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.form if request.method == 'POST' else request.args
            missing_params = []
            for arg in required_args:
                if arg not in data:
                    missing_params.append(arg)
            if missing_params:
                return gen_result_missing_param(missing_params)
            else:
                return func(data=data, *args, **kwargs)
        return wrapper
    return decorator

def disabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return gen_result_failure(message='API call disabled!')
    return wrapper

def gen_result_success(data=None, message=None):
    result = OrderedDict([
        ('success', True)])
    if message is not None:
        result['message'] = message
    if data is not None:
        result['data'] = data
    return result

def gen_result_failure(message=None):
    result = OrderedDict([
        ('success', False)])
    if message is not None:
        result['message'] = message
    return result

def gen_result_missing_param(params):
    missingparamsstring = ', '.join(params)
    return gen_result_failure('Missing parameters: ' + missingparamsstring)