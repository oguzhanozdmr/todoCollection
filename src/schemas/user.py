'''Model validates'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python

from marshmallow import (fields,
                         validate,
                         Schema)


class UserLogin(Schema):
    email = fields.Str(
        required=True,
        validate=validate.Email(error="Not a valid email address")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=6,
            max=120,
            error="password must be minimum 6 and max 10 characters"
        ),
        load_only=True
    )


class UserRegister(UserLogin):
    name_surname = fields.Str(
        required=True,
        validate=validate.Length(
            min=3,
            max=100,
            error="name_surname must be minimum 3 and max 100 characters"
        ),
    )
