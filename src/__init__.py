# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import environ
from flask import Flask


__all__ = ['create_app']

__author__ = "Oguzhan Ozdemir"
__status__ = environ.get('deployment_status')


def create_app() -> Flask: 
    app = Flask(__name__)
    app.secret_key = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    
    return app
