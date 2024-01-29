import unittest
import json
from unittest.mock import patch
from app import app


class TestTaskEndpoint(unittest.TestCase):
    """
    Class Task Testing
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("src.task.create_task")
    def test_create_task_success(self, mock_create_task_cmd):
        """Create Task Testing"""

        result = {"result": {"id": 19, "name": "任務名稱", "status": 0}}

        mock_create_task_cmd.return_value = result

        # Send a CREATE request to the endpoint
        post_data = {"name": "任務名稱"}
        response = self.app.post(
            "/task", data=json.dumps(post_data), content_type="application/json"
        )

        # Assert the status code and response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), result)

    @patch("src.task.create_task")
    def test_create_task_not_success(self, mock_create_task_cmd):
        """Create Task Testing"""

        result = {"result": "Input Error!"}

        mock_create_task_cmd.return_value = result

        # Send a CREATE request to the endpoint with missing name field
        data_missing_name = {}

        response_missing_name = self.app.post(
            "/task",
            data=json.dumps(data_missing_name),
            content_type="application/json",
        )

        # Assert the status code for a request with missing name field
        self.assertEqual(response_missing_name.status_code, 200)
        self.assertEqual(json.loads(response_missing_name.data), result)

    @patch("src.task.update_task")
    def test_update_task_success(self, mock_update_task_cmd):
        """Update Task Testing"""

        result = {"result": "Task updated successfully"}

        mock_update_task_cmd.return_value = result

        # Send a UPDATE request to the endpoint
        put_data = {"id": 5, "name": "任務名稱", "status": 1}
        response = self.app.put(
            "/task/5", data=json.dumps(put_data), content_type="application/json"
        )

        # Assert the status code and response
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(json.loads(response.data), result)

    @patch("src.task.update_task")
    def test_update_task_not_success(self, mock_update_task_cmd):
        """Update Task Testing"""

        result = {"result": "Record is not exist!"}

        mock_update_task_cmd.return_value = result

        # Send a UPDATE request to the endpoint for a non-existent task
        data_non_existent = {"id": 999, "name": "Updated Task", "status": 1}
        response_non_existent = self.app.put(
            "/task/999",
            data=json.dumps(data_non_existent),
            content_type="application/json",
        )

        # Assert the status code for a non-existent task
        self.assertEqual(response_non_existent.status_code, 200)
        self.assertEqual(json.loads(response_non_existent.data), result)

    @patch("src.task.delete_task")
    def test_delete_task_success(self, mock_delete_task_cmd):
        """Delete Task Testing"""

        result = {"result": "1 record(s) deleted."}

        mock_delete_task_cmd.return_value = result

        # Send a DELETE request to the endpoint
        response = self.app.delete("/task/4")

        # Assert the status code and response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), result)

    @patch("src.task.delete_task")
    def test_delete_task_not_exist(self, mock_delete_task_cmd):
        """Task is not exist!"""
        result = {"result": "Record is not exist!"}

        mock_delete_task_cmd.return_value = result

        # Send a DELETE request to the endpoint with a non-existent task ID
        response = self.app.delete("/task/999")  # Use a non-existent task ID

        # Assert the status code and response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), result)

    def test_delete_task_input_error(self):
        """Send a DELETE request without providing an ID"""
        response = self.app.delete("/task")

        # Assert the status code and response
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
