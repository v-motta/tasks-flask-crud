from flask import Flask, request, jsonify
from models.task import Task
from uuid import uuid4

app = Flask(__name__)

tasks = []

@app.route("/tasks", methods=["POST"])
def create_tasks():
  data = request.get_json()
  new_task = Task(uuid4(), data.get('title'), data.get('description', ''))
  tasks.append(new_task)
  print(tasks)
  return jsonify({"message": "Task created successfully", "id": new_task.id}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
  return jsonify({
    "tasks": [task.to_dict() for task in tasks],
    "count": len(tasks)
  })

@app.route("/tasks/<uuid:task_id>", methods=["GET"])
def get_task(task_id):
  task = next((task for task in tasks if task.id == task_id), None)
  if task:
    return jsonify(task.to_dict())
  else:
    return jsonify({"message": "Task not found"}), 404

@app.route("/tasks/<uuid:task_id>", methods=["PUT"])
def update_task(task_id):
  data = request.get_json()
  task = next((task for task in tasks if task.id == task_id), None)
  if task:
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    return jsonify({"message": "Task updated successfully"}), 200
  else:
    return jsonify({"message": "Task not found"}), 404
  
@app.route("/tasks/<uuid:task_id>", methods=["DELETE"])
def delete_task(task_id):
  task = next((task for task in tasks if task.id == task_id), None)
  if task:
    tasks.remove(task)
    return jsonify({"message": "Task deleted successfully"}), 200
  else:
    return jsonify({"message": "Task not found"}), 404

if __name__ == "__main__":
  app.run(debug=True)
