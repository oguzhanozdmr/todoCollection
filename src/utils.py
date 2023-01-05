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
from marshmallow import ValidationError, INCLUDE
from src.models import HttpType

JWT_KEY = '_E?y-kEN2$rB=6=!nWweFzU7uHWbs-w&TV=wpR@DmdwwWuEr46tQXy5mCbEuChya'
JWT_ALGORITHM = 'HS256'
# TODO: Read Config


def create_token(email: str,
                 expire_time_as_minute: Union[int, None] = None,
                 **kwargs) -> str:
    _expire_time_as_minute = expire_time_as_minute if expire_time_as_minute else 24 * 60 * 60
    now = time.time()
    expire = now + (60 * _expire_time_as_minute)

    claims = {
        "iat": now,
        "exp": expire,
        "mail": email
    } | kwargs
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

class validate_json_body():
    def __init__(self, schema):
        self.schema = schema
        self.caller_path = inspect.stack()[1][1]

    def __call__(self, fn):
        @wraps(fn)
        def validate(*args, **kwargs):
            json_data = request.get_json(force=True)
            try:
                data = self.schema.load(
                    json_data,
                    unknown=INCLUDE
                )
            except ValidationError as ex:
                return error_as_json(
                    msg='Unvalid json body.',
                    exception_type=ex,
                    detail=ex.messages,
                    func_path=self._caller_path(fn.__name__)), HttpType.NOT_VALIDATE_JSON_BODY.value
            return fn(data=data, *args, **kwargs)
        return validate
    
    def _caller_path(self, func_name: str) -> str:
        proje_path = f"{Path.cwd()}/"
        path = self.caller_path.replace(
            proje_path, ''
        ).replace( '.py', '').replace('/', '.')
        return f'{path}.{func_name}'

def get_caller_path(caller) -> str:
    proje_path = f"{Path.cwd()}/"
    path = caller[1].replace(proje_path, '').replace(
        '.py', '').replace('/', '.')
    return f'{path}.{caller[3]}'

def error_as_json(msg: str,
                  exception_type: Exception = None,
                  detail: str = None,
                  func_path = None,
                  **kwargs) -> Response:
    _msg = {
        'status': 'Error',
        'message': msg,
    } | kwargs

    if bool(environ.get('DEBUG')):
        _msg['detail'] = detail
        if exception_type:
            _msg['type'] = exception_type.__class__.__name__
        _msg['code'] = get_caller_path(inspect.stack()[1]) if not func_path else func_path
    return jsonify(_msg)
