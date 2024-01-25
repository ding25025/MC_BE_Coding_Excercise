"""task function."""
import json
import unittest
from flask import request, Blueprint

task_bp = Blueprint("task", __name__)


# task List
@task_bp.route("/tasks", methods=["GET"])
def taskList():
    """
    Get Task List
    Retrieve Task list
    ---
    tags:
      - Task APIs
    produces: application/json,

    responses:
      401:
        description: 401 error
      200:
        description: Retrieve task list
        examples:
          task-list:{
            result:[{"id": 1, "name": "taskname", "status": 0}]
            }
    """
    result = ""

    return result


# create task
@task_bp.route("/", methods=["POST"])
def createTask():
    """
    create task information
    ---
    tags:
      - task APIs
    produces: application/json,
    parameters:
    - name: taskname
      in: body
      required: true
      schema:
        id: taskid
        required:
          - name
        properties:
          id:
            type: string
            description: 任務流水號
          name:
            type: string
            description: 任務名稱
          status:
            type: bool
            description: 任務狀態
    responses:
      401:
        description: Unauthorized error
      201:
        description: Create Success

    """
    content = request.data.decode()
    data = json.loads(content)
    print(data)

    result = insertTask(data["name"])

    return result


@task_bp.route("/", methods=["PUT"])
# update task
def updateTask():
    """
    update task
    ---
    tags:
      - User APIs
    produces: application/json,
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
          name:
            type: string
            description: name
          status:
            type: bool
            description: O:Incomplete 1:Complete


    responses:
      401:
        description: Unauthorized error
      200:
        description: Update Success
        examples:
          task : {"id": 1, "name": "taskname", "status": 1}
    """
    content = request.data.decode()
    data = json.loads(content)

    if "name" not in data:
        msg = msgresult(False, str(errorCode["1007"]) + "=>Email ", "1007", "", "")
        return msg

    userInfo = result["result"]
    print(userInfo)
    if len(userInfo) > 0:
        return result
    else:
        msg = msgresult(False, str(errorCode["1008"]), "1008", "", "")
        return msg


# delete task
@task_bp.route("/", methods=["Delete"])
def deleteTask():
    """
    Delete Task
    ---
    tags:
      - Delete Task APIs
    produces: application/json,
    parameters:
    - name: id
      in: query
      type: string
      required: true
    responses:
      401:
        description: Unauthorized error
      200:
        description: Delete Task
        examples:
          task's id: [{"id":1}]
    """
    id = request.args.get("id")
    print(id)

    if id is None:
        msg = msgresult(
            False,
            str(Errorcode["1007"]) + "=>Invalid id ",
            "1007",
            "",
            "",
        )
        return msg
    else:
        result = deleteTaskExcute(id)
        return result
