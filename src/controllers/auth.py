'''Auth service controller'''
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# TODO: Devoploment modu icin HATEOAS mimarisi kullanilabilir

from flask import Blueprint, jsonify, request

from src.black_list import BLACK_LIST
from src.decorators import authorized, validate_json_body
from src.models import HttpType
from src.models.user import UserModel
from src.schemas import user_login_schema, user_register_schema

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST'])
@validate_json_body(user_register_schema)
def register(data: dict):
    """user register"""
    user = UserModel(
        email=data['email'],
        name_surname=data['name_surname'],
        password=data['password']
    )
    user.save_to_db()
    return jsonify({
        'status': 'Success',
        'mesage': 'Your account has been successfully created.'
    }), 201


@auth_blueprint.route('/login', methods=['POST'])
@validate_json_body(user_login_schema)
def login(data: dict):
    """user login"""
    user = UserModel.find_by_email(data['email'])        
    # TODO: User olmamasini kontrol et
    if user.verify_password(data['password']):
        return jsonify({
            'status': 'Success',
            'message': 'Login is succesfuly',
            'token': user.genarete_acces_token()
        }), HttpType.OK.value
        # TODO: oath kullanbilir access ve refresh token donebilir.
    return jsonify({
        'status': 'Unsuccessful',
        'message': 'Email or password wrong!',
    }), HttpType.OK.BAD_REQUEST


@auth_blueprint.route('/logout', methods=['POST'])
@authorized()
def logout(**kwargs):
    """user logout"""
    authorization_data = request.headers.get('Authorization', '')
    token = str.replace(str(authorization_data), 'Bearer ', '')
    BLACK_LIST.add(token)
    return jsonify({
        'status': 'Success',
        'message': 'Logout is succesfuly',
    })
