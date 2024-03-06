from flask import Flask, jsonify, request, abort, make_response
from datetime import datetime
from flask_expects_json import expects_json

from jsonschema import ValidationError


app = Flask(__name__)


tasks = []

schema = {
    'name': {'type': 'string',  "minLength": 1, "maxLength": 40},
    'category': {'type': 'string',  "minLength": 1, "maxLength": 40},
    'required': ['name', 'category']
}

BASE_URL = '/api/v1/'
@app.route('/')
def home():
    return 'Welcome to my to-do list'


@app.route(BASE_URL+'tasks', methods=['POST'])
@expects_json(schema)
def create_task():
    if not request.json:
        abort(404)
    print(request.json)
    this_time = datetime.now()
    task = {
        'id': len(tasks) + 1,
        'name': request.json['name'],
        'category': request.json['category'],
        'status': False,
        'created': this_time,
        'updated': this_time

    }

    tasks.append(tasks)
    return jsonify({'task': task}), 201 #No olvides cambiar uwu

@app.route(BASE_URL+ 'tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks':tasks})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found')

    return jsonify({"task": this_task[0]})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def check_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404)
    tasks[this_task[0].id]['status'] = not this_task[0]['status']
    return jsonify({"task": this_task[0].id})


@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404)
    tasks.remove(this_task[0])
    return jsonify({'result': True})


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'Error, incorrect .json schema. Please insert name and category': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error


if __name__ == '__main__':
    app.run(debug=True)