'''Model validates'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python
import inspect
from functools import wraps
from pathlib import Path

import jwt
from flask import request
from marshmallow import ValidationError, INCLUDE
from src.models import HttpType, UserType
from src.models.user import UserModel
from src.black_list import BLACK_LIST
from src.utils import error_as_json, JWT_KEY, JWT_ALGORITHM

JWT_KEY = '_E?y-kEN2$rB=6=!nWweFzU7uHWbs-w&TV=wpR@DmdwwWuEr46tQXy5mCbEuChya'
JWT_ALGORITHM = 'HS256'
# TODO: Read Config


def caller_path(caller_path: str, func_name: str) -> str:
    proje_path = f"{Path.cwd()}/"
    path = caller_path.replace(
        proje_path, ''
    ).replace('.py', '').replace('/', '.')
    return f'{path}.{func_name}'


class authorized():
    def __init__(self,
                 user_type: UserType = UserType.AUTHENTICATED,
                 required_permission: set = ()):

        self.user_type = user_type
        self._permission = required_permission
        self.caller_module_path = inspect.stack()[1][1]

    def __call__(self, fn):
        @wraps(fn)
        def verify_permison(*args, **kwargs):
            if self.user_type == UserType.ANONYMOUS:
                return fn(current_user=None, *args, **kwargs)

            authorization_data = request.headers.get('Authorization', '')
            token = str.replace(str(authorization_data), 'Bearer ', '')
            try:
                if token in BLACK_LIST:
                    raise jwt.exceptions.InvalidTokenError('Invalid token')

                decoded_token = jwt.decode(
                    str(token),
                    JWT_KEY,
                    algorithms=[JWT_ALGORITHM]
                )
            except jwt.exceptions.InvalidTokenError as ex:
                return error_as_json(
                    msg='Invalid token',
                    exception_type=ex,
                    detail=str(ex),
                    func_path=caller_path(self.caller_module_path, fn.__name__)
                ), HttpType.Unauthorized.value
            # TODO: Rolecheck
            return fn(
                       current_user=UserModel.find_by_email(decoded_token['email']),
                       *args,
                       **kwargs
                )
        return verify_permison


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
                    func_path=self._caller_path(fn.__name__)
                ), HttpType.NOT_VALIDATE_JSON_BODY.value
            return fn(data=data, *args, **kwargs)
        return validate
