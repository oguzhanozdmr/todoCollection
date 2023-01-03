'''Auth service controller'''
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__, url_prefix='auth')

def register():
    """user register"""
    ...

def login():
    """user login"""
    ...

def me():
    """get me info"""
    ...

def get_access_token():
    """get user accces token"""
    ...
