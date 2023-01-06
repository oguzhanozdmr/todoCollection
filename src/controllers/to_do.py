# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import Blueprint, jsonify, request, url_for

from src.models.to_do import TodoModel
from src.models.user import UserModel
from src.schemas import to_do_schema, to_do_input_schema
from src.decorators import authorized, validate_json_body


to_do_blueprint = Blueprint('to_do', __name__, url_prefix='/todos')


# GET Fetch a random todo record
DOMAIN = 'http://localhost:8080'

@to_do_blueprint.route('/', methods=['GET'])
@authorized()
def list_task(**kwargs):
    current_user = kwargs.get('current_user')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    todo_list = TodoModel.find_by_user_id(
        user_id=current_user.id,
        page=page,
        per_page=per_page
    )
    
    next_page_url = None
    previos_page = None
    
    if page < todo_list.pages:
        next_page_url = f'{DOMAIN}{url_for("to_do.list_task", page=page+1)}'
       
    if page > 1:
        previos_page = f'{DOMAIN}{url_for("to_do.list_task", page=page-1)}'

    return jsonify({
        "current_page": page,
        "item_list":  to_do_schema.dump(todo_list, many=True),
        "previos_page" : previos_page,
        "next_page" : next_page_url,
        "page_count": todo_list.pages,
        "total_count": todo_list.total
    })

@to_do_blueprint.route('/random', methods=['GET'])
@authorized()
def random_task(**kwargs):
    current_user = kwargs.get('current_user')
    todo = TodoModel.find_by_random(user_id=current_user.id)
    return jsonify(to_do_schema.dump(todo))

@to_do_blueprint.route('/<int:todo_id>', methods=['GET'])
@authorized()
def find_by_id_task(todo_id: int, **kwargs):
    current_user = kwargs.get('current_user')
    todo = TodoModel.find_by_id(id=todo_id, user_id=current_user.id)
    if not todo:
        return jsonify({'msg': 'task not found'}), 404
    return jsonify(to_do_schema.dump(todo))

@to_do_blueprint.route('/<int:todo_id>', methods=['DELETE'])
@authorized()
def delete_task(todo_id: int, **kwargs):
    current_user = kwargs.get('current_user')
    todo = TodoModel.find_by_id(id=todo_id, user_id=current_user.id)
    todo.delete_from_db()
    return jsonify({'status': 'Success', 'message': 'Task deleted successfully'})
    
@to_do_blueprint.route('/<int:todo_id>', methods=['PUT'])
@authorized()
@validate_json_body(to_do_input_schema)
def update_task(todo_id: int, **kwargs):
    current_user = kwargs.get('current_user')
    data = kwargs.get('data')

    todo = TodoModel.find_by_id(id=todo_id, user_id=current_user.id)
    #TODO: Yoksa hata don
    todo.heading = data.get('heading')
    todo.description = data.get('description')
    todo.save_to_db()
    return jsonify({'status': 'Success', 'message': 'Task updated successfully'})
    
@to_do_blueprint.route('/', methods=['POST'])
@authorized()
@validate_json_body(to_do_input_schema)
def create_task(**kwargs):
    current_user = kwargs.get('current_user')
    data = kwargs.get('data')
    
    todo = TodoModel(
        heading=data['heading'],
        description=data['description'],
        user=current_user
    )
    todo.save_to_db()
    return jsonify({
        'status': 'Success',
        'message': 'Task created successfully'
    })
