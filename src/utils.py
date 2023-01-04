'''Model validates'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python
import inspect
import time
from functools import wraps
from os import environ
from pathlib import Path
from typing import Union

import jwt
from flask import Response, jsonify, request

JWT_KEY = '_E?y-kEN2$rB=6=!nWweFzU7uHWbs-w&TV=wpR@DmdwwWuEr46tQXy5mCbEuChya'
JWT_ALGORITHM = 'HS256'
# TODO: Read Config


def create_token(mail: str, expire_time_as_minute: Union[int, None] = None, **kwargs) -> str:
    _expire_time_as_minute = expire_time_as_minute if expire_time_as_minute else 24 * 60 * 60
    # TODO: Read Config
    now = time.time()
    expire = now + (60 * _expire_time_as_minute)

    claims = {
        "iat": now,
        "exp": expire,
        "mail": mail
    }
    token = jwt.encode(claims, key=JWT_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    try:
        claims = jwt.decode(str(token), JWT_KEY, algorithms=[JWT_ALGORITHM])
        return {'status': True, 'data': claims}
    except Exception as ex:
        return {'status': False, 'error': ex}


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_data = request.headers.get('Authorization', '')
        token = str.replace(str(authorization_data), 'Bearer ', '')
        if not token:
            return error_as_json(msg='Token is missing'), 401

        if not decode_token(token)['status']:
            return error_as_json(msg='Token is expired'), 401
        return f(*args, **kwargs)
    return decorated_function

# TODO: rolecheck


def validate_json_body(schema):
    def inner_func(f):
        @wraps(f)
        def validate(*args, **kwargs):
            return f(*args, **kwargs)
        return validate
    return inner_func


def get_caller_path(caller) -> str:
    proje_path = f"{Path.cwd()}/"
    path = caller[1].replace(proje_path, '').replace(
        '.py', '').replace('/', '.')
    return f'{path}.{caller[3]}'


def error_as_json(msg: str,
                  exception_type: Exception = None,
                  detail: str = None, **kwargs) -> Response:
    _msg = {
        'status': 'Error',
        'message': msg,
    } | kwargs
    if bool(environ.get('DEBUG')):
        _msg['detail'] = detail
        if exception_type:
            _msg['type'] = exception_type.__class__.__name__
        _msg['code'] = get_caller_path(inspect.stack()[1])
    return jsonify(_msg)
