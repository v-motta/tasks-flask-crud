import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
  new_task_data = {
    "title": "Test Task",
    "description": "This is a test task.",
  }
  response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)
  assert response.status_code == 201

  response_data = response.json()
  assert "message" in response_data
  assert "id" in response_data

  tasks.append(response_data["id"])

def test_get_tasks():
  response = requests.get(f'{BASE_URL}/tasks')
  assert response.status_code == 200
  
  response_data = response.json()
  assert "tasks" in response_data
  assert "count" in response_data

def test_get_task():
  if tasks:
    task_id = tasks[0]
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    
    response_data = response.json()
    assert task_id == response_data["id"]

def test_update_task():
  if tasks:
    task_id = tasks[0]
    updated_task_data = {
      "title": "Updated Test Task",
      "description": "This is an updated test task.",
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=updated_task_data)
    assert response.status_code == 200

    response_data = response.json()
    assert "message" in response_data

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200

    response_data = response.json()
    assert updated_task_data["title"] == response_data["title"]
    assert updated_task_data["description"] == response_data["description"]

def test_delete_task():
  if tasks:
    task_id = tasks[0]
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404
