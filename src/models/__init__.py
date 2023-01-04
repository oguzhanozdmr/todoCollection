# -*- coding: utf-8 -*-
#!/usr/bin/env python

from enum import Enum


class StatusType(Enum):
    DELETED = 0
    ACTIVE = 1
    CONFIRMED = 2
    
class HttpType(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 200
    NOT_VALIDATE_JSON_BODY = 422    
