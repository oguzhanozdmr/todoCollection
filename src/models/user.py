'''Flask extensions file'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python
#pylint: disable=C0115, C0116, E0611

from typing import List
from werkzeug.security import (check_password_hash,
                                generate_password_hash)
from src.extensions import db
from src.models import StatusType
from src.utils import create_token

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(250),
        unique=True,
        nullable=False
    )
    name_surname = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    password_hash = db.Column(
        db.String(120),
        unique=False,
        nullable=False
    )
    status = db.Column(
        db.Enum(StatusType),
        default=StatusType.ACTIVE
    )
    created_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    #TODO: perfomans icin name_username ve mailin adresinin indexlenmesi
    def __init__(self,
                email: str,
                name_surname: str,
                password: str) -> 'UserModel':
        self.email= email
        self.name_surname = name_surname
        self.password = password

    @property
    def password(self):
        raise AttributeError('Password is not a readable attritube!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def genarete_acces_token(self):
        #TODO: Read Role info
        return create_token(self.email, name_surname=self.name_surname)

    def __repr__(self):
        return f'User<name_username:{self.name_surname},' \
                f'email: {self.email}, id:{self.id}>'

    @classmethod
    def search_by_name_name_or_email(cls,
                                     search_txt: str,
                                     page:int = 1,
                                     per_page: int = 5) -> 'UserModel':
        #TODO: ElasticSearch ile aranmali
        return cls.query.filter(
            cls.email.like(search_txt) | cls.name_surname.like
            ).paginate(page, per_page,error_out=False)

    @classmethod
    def find_by_email(cls, email: str) -> 'UserModel':
        return cls.query.filter_by(status=StatusType.ACTIVE,
                                    email=email).first()

    @classmethod
    def find_by_all(cls) -> List['UserModel']:
        return cls.query.filter_by(status=StatusType.ACTIVE).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    #sqlalchemy ekstra guvenlik icin validates kullanilabilir.