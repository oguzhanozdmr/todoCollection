# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import environ
from flask import Flask, jsonify
from src.utils import error_as_json
from src.extensions import db

__all__ = ['create_app']
__author__ = "Oguzhan Ozdemir"


def create_app() -> Flask: 
    app = Flask(__name__)
    app.secret_key = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    
    db.init_app(app)
    
    register_blueprints(app)
    register_error_handler(app)
    create_db_all(app)

    return app

def register_blueprints(app: Flask):
    from src.controllers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from src.controllers.to_do import to_do_blueprint
    app.register_blueprint(to_do_blueprint)

def register_error_handler(app: Flask):
    @app.errorhandler(400)
    def bad_request(e):
        return error_as_json(msg="invalid request"), 400
    
    @app.errorhandler(404)
    def not_found_url(e):
        return error_as_json(msg="invalid request"), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return error_as_json(
            msg="Method Not Allowed",
            detail="The method is not allowed for the requested URL."), 405

def create_db_all(app: Flask):
    from src.models import to_do, user
    
    with app.app_context():
        db.create_all()
