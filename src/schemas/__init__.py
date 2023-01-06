'''Model validates'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python


from src.schemas.user import UserLogin, UserRegister
from src.schemas.to_do import Todo, TodoInput

user_login_schema = UserLogin()
user_register_schema = UserRegister()

to_do_schema = Todo()
to_do_input_schema = TodoInput()
