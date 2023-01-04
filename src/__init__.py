# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import environ
from flask import Flask, jsonify
from src.utils import error_as_json
from src.extensions import db

__all__ = ['create_app']

__author__ = "Oguzhan Ozdemir"
__status__ = environ.get('deployment_status')


def create_app() -> Flask: 
    app = Flask(__name__)
    app.secret_key = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql://skydata:pvFQMzdN*2Ky@localhost:5432/skyadatabase')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    
    db.init_app(app)
    register_blueprints(app)
    
    @app.errorhandler(400)
    def bad_request(e):
        return error_as_json(msg="invalid request"), 400
    
    return app

def register_blueprints(app: Flask):
    from src.controllers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

