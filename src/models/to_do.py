'''Flask extensions file'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python
# pylint: disable=C0115, C0116, E0611


import datetime
from typing import List
from src.extensions import db
from src.models import StatusType, ToDoStatus
from src.models.user import UserModel

# TODO: Proje yapisi olusturulmali


class TodoModel(db.Model):
    __tablename__ = "to_do"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    heading = db.Column(
        db.String(120),
        unique=False,
        nullable=False
    )
    description = db.Column(
        db.String(250),
        unique=False,
        nullable=True
    )
    todo_status = db.Column(
        db.Enum(ToDoStatus),
        default=ToDoStatus.TODO
    )
    status = db.Column(
        db.Enum(StatusType),
        default=StatusType.ACTIVE
    )
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    modefiend_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __init__(self,
                 heading: str,
                 user: UserModel,
                 description: str = '',
                 ) -> None:
        self.heading = heading
        self.description = description
        self.created_by = user.id

    @classmethod
    def find_by_user_id(cls,
                        user_id: int,
                        page: int = 1,
                        per_page: int = 1) -> List['TodoModel']:
        return cls.query.filter_by(
            status=StatusType.ACTIVE,
            created_by=user_id
        ).order_by(
            cls.created_date
        ).paginate(page=page, per_page=per_page)

    @classmethod
    def find_by_id(cls, id: int, user_id) -> 'TodoModel':
        return cls.query.filter_by(status=StatusType.ACTIVE,
                                   created_by=user_id,
                                   id=id).first()

    def save_to_db(self) -> None:
        now = datetime.datetime.utcnow()
        self.modefiend_date = now.strftime('%Y-%m-%d %H:%M:%S')

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        self.status = StatusType.DELETED
        self.save_to_db()

    def __repr__(self) -> str:
        return f'<Todo id:{self.id} heading:{self.heading}>'
