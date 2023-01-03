'''Model validates'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
import jwt
from functools import wraps
from flask import request, jsonify


JWT_KEY = '_E?y-kEN2$rB=6=!nWweFzU7uHWbs-w&TV=wpR@DmdwwWuEr46tQXy5mCbEuChya'
JWT_ALGORITHM = 'HS256'
#TODO: Read Config


def create_token(mail: str, **kwargs) -> str:  
    expire_as_minute = 24 * 60 * 60
    #TODO: Read Config
    now = time.time() 
    expire = now + (60 * expire_as_minute)

    claims = {
        "iat": now,
        "exp": expire,
        "mail": mail
    }
    token = jwt.encode(claims,key=JWT_KEY, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token: str) -> dict:
    try:
        claims = jwt.decode(str(token), JWT_KEY, algorithms=[JWT_ALGORITHM])
        return {'status': True, 'data': claims}
    except Exception as ex:
        return {'status': False, 'error': ex}

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        authorization_data = request.headers.get('Authorization', '')
        token = str.replace(str(authorization_data), 'Bearer ','')
        if not token:
            return jsonify({'msg': 'Token is missing'}), 401

        if not decode_token(token)['status']:
            return jsonify({
                'name': 'GECERESIZ',
                'msg': 'Süresi dolmuş ve/veya geçersiz.'
                }), 401
        return f(*args, **kws)            
    return decorated_function
