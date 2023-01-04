'''Model validates'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python


from src.schemas.user import UserLogin, UserRegister


user_login_schema = UserLogin()
user_register_schema = UserRegister()
