"""task function."""
import json
import unittest
from flask import request, Blueprint
from DBConn import getTasks, insertTaskCmd, updateTaskCmd, deleteTaskCmd

task_bp = Blueprint("task", __name__)


# task List
@task_bp.route("", methods=["GET"])
def taskList():
    """
    Get Task List
    Retrieve Task list
    ---
    tags:
      - Task APIs
    responses:
      401:
        description: 401 error
      200:
        description: Retrieve task list
        examples:
          task-list:{result:[{"id": 1,"name":"taskname", "status":0}]}
    """
    result = getTasks()

    return result


# create task
@task_bp.route("", methods=["POST"])
def createTask():
    """
    create task information
    ---
    tags:
      - Task APIs
    summary: Create task
    description: Create a a task
    parameters:
      - name: taskname
        in: body
        required: true

    responses:
      401:
        description: Unauthorized error
      201:
        description: Create Success
    """
    content = request.data.decode()
    data = json.loads(content)
    print(data)

    if "name" not in data:
        msg = {"result": "Input Error!"}
        return msg
    result = insertTaskCmd(data["name"])

    return result


@task_bp.route("/<int:id>", methods=["PUT"])
# update task
def updateTask(id):
    """
    update task
    ---
    tags:
      - Task APIs
    summary: Update task by ID
    description: Update a task
    parameters:
    - name: task
      in: body
      required: true
      schema:
        id: task
        required:
          - name
          - status
        properties:
          id:
            type: integer
            description: 任務序號
          name:
            type: string
            description: 任務名稱
          status:
            type: boolean
            description: 任務狀態 O:Incomplete 1:Complete
    responses:
      '401':
        description: Unauthorized error
      '200':
        description: Update Success
        examples:
          task : {"id": 1, "name": "taskname", "status": 1}
    """
    content = request.data.decode()
    data = json.loads(content)
    print(data)
    if id is None or "name" not in data or "status" not in data:
        msg = {"result": "Input Error!"}
        return msg
    result = updateTaskCmd(id, data["name"], data["status"])

    return result


# delete task
@task_bp.route("/<int:id>", methods=["Delete"])
def deleteTask(id):
    """
    Delete Task
    ---
    tags:
      - Task APIs
    summary: Find task by ID
    description: Delete a task
    parameters:
      - name: id
        in: path
        required: true
        schema:
            type: integer
            format: int64
    responses:
      '401':
        description: Unauthorized error
      '200':
        description: Delete Task
    """
    if id is None:
        msg = {"result": "Input Error!"}
        return msg
    else:
        result = deleteTaskCmd(id)
        return result
