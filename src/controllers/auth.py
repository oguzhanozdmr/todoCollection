'''Auth service controller'''
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import Blueprint, request, jsonify


from src.black_list import BLACK_LIST
from src.utils import authorize, validate_json_body
from src.schemas import user_register_schema, user_login_schema
from src.models import HttpType
from src.models.user import UserModel

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST'])
@validate_json_body(user_register_schema)
def register(data):
    """user register"""
    user = UserModel(
        email=data['email'],
        name_surname=data['name_surname'],
        password=data['password']
    )
    # user.save_to_db()
    # TODO: DB error handling
    # TODO: Kullanici zaten var uyarisi
    return jsonify({
        'status': 'Success',
        'mesage': 'Your account has been successfully created.'
    }), 201


@auth_blueprint.route('/login', methods=['POST'])
@validate_json_body(user_login_schema)
def login(data):
    """user login"""
    user = UserModel.find_by_email(data['email'])
    #TODO: User olmamasini kontrol et
    if user.verify_password(data['password']):
        return jsonify({
            'status': 'Success',
            'message': 'Login is succesfuly',
            'token': user.genarete_acces_token()
        }), HttpType.OK.value
        #TODO: oath kullanbilir access ve refresh token donebilir.
        ... #return access succes
    return jsonify({
            'status': 'Unsuccessful',
            'message': 'Email or password wrong!',
        }), HttpType.OK.BAD_REQUEST
    # return access false


@auth_blueprint.route('/logout', methods=['POST'])
@authorize
def logout(user_info: dict=None):
    """user logout"""
    BLACK_LIST.add()
    ...


@auth_blueprint.route('/me', methods=['GET'])
@authorize
def me():
    """get me info"""
    ...
