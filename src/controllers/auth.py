'''Auth service controller'''
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, INCLUDE

from src.black_list import BLACK_LIST
from src.utils import authorize, error_as_json
from src.schemas import user_register_schema
from src.models import HttpType
from src.models.user import UserModel

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST'])
def register(data):
    """user register"""
    json_data = request.get_json(force=True)

    try:
        data = user_register_schema.load(json_data, unknown=INCLUDE)
    except ValidationError as ex:
        return error_as_json(msg='Unvalid json body.',
                             exception_type=ex,
                             detail=ex.messages), HttpType.NOT_VALIDATE_JSON_BODY.value
    user = UserModel(
        email=data['email'],
        name_surname=data['name_surname'],
        password=data['password']
    )
    user.save_to_db()
    # TODO: DB error handling
    return jsonify({
        'status': 'Success',
        'mesage': 'Your account has been successfully created.'
    }), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """user login"""
    json_data = request.get_json(force=True)


@auth_blueprint.route('/logout', methods=['POST'])
@authorize
def logout():
    """user logout"""
    BLACK_LIST.add()
    ...


@auth_blueprint.route('/me', methods=['GET'])
@authorize
def me():
    """get me info"""
    ...
