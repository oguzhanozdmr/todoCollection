from src.models.to_do import TodoModel
from src.models.user import UserModel
from marshmallow import (fields,
                         validate,
                         Schema,
                         ValidationError,
                         validates)


"""  id = db.Column(
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
    )"""

class Todo(Schema):
    id = fields.Int()
    heading = fields.Str()
    description = fields.Str()
    todo_status = fields.Str(
        data_key='status'
    )
    created_by = fields.Str()
    created_date = fields.Str()
    
class TodoInput(Schema):
    heading = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            max=120,
            error="heading must be minimum 1 and max 120 characters"
        ),
    )
    description = fields.Str(
        validate=validate.Length(
            min=0,
            max=250,
            error="description must be max 250 characters"
        ),
    )
