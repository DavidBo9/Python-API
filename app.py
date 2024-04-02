from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status
        }

@app.route('/')
def index():
    return 'Welcome to my ORM App'

@app.route('/create_task', methods=['POST'])
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    task = Task(name=request.json['name'], status=request.json.get('status', False))
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    return jsonify(task.to_dict())

@app.route('/tasks_update/<int:task_id>', methods=['GET'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    task.status = not task.status
    return jsonify(task.to_dict())

@app.route('/tasks_delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'status':True}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created...")

    app.run(debug=True)
