# -*- coding: utf-8 -*-
#!/usr/bin/env python

from enum import Enum, auto


class StatusType(Enum):
    DELETED = auto()
    ACTIVE = auto()
    CONFIRMED = auto()
    
class HttpType(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 200
    Unauthorized = 401
    NOT_VALIDATE_JSON_BODY = 422

class UserType(Enum):
    ANONYMOUS = auto()
    AUTHENTICATED = auto()

class ToDoStatus(Enum):
    TODO = auto()
    INPROGRESS = auto()
    DONE = auto()
