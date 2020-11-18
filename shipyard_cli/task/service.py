"""
Business logic for task related operations.
"""

import io
import json
import os
from http import HTTPStatus
from typing import List

import bson
import requests
from shipyard_cli.errors import StatusError
from shipyard_cli.task.model import Task


class TaskService():
    """Service for task operations."""

    def __init__(self, url: str, port: str):
        self.base_url = url + ':' + port

    def get_all(self) -> List[Task]:
        """Obtain the list of tasks."""

        response = requests.get(self.base_url + '/tasks')
        if response.status_code == HTTPStatus.OK:
            return Task.Schema().load(response.json(), many=True)
        else:
            raise StatusError(response.json()['error'])

    def get_one(self, task_key: str) -> Task:
        """
        Obtain detailed information about a task.

        The given task key can be either its ID or name.
        """

        if bson.ObjectId.is_valid(task_key):
            uri = '/tasks/' + task_key
        else:
            uri = '/tasks?name=' + task_key
        response = requests.get(self.base_url + uri)
        if response.status_code == HTTPStatus.OK:
            return Task.Schema().load(response.json())
        else:
            raise StatusError(response.json()['error'])

    def create(self, task: Task, file: io.BufferedReader) -> str:
        """Create a new task."""

        response = requests.post(
            self.base_url + '/tasks',
            files={
                'file': (os.path.basename(file.name), file),
                'specs': (None, Task.Schema(exclude=['_id']).dumps(task), 'application/json')
            }
        )
        if response.status_code == HTTPStatus.OK:
            return response.json()['_id']
        else:
            raise StatusError(response.json()['error'])

    def update(self, task_key: str, new_values: dict, new_file: io.BufferedReader) -> Task:
        """
        Change the values of a task.

        The given task key can be either its ID or name.
        """

        if not bson.ObjectId.is_valid(task_key):
            response = requests.get(self.base_url + '/tasks?name=' + task_key)
            if response.status_code != HTTPStatus.OK:
                raise StatusError(response.json()['error'])
            task_key = response.json()['_id']

        files = {'specs': (None, json.dumps(new_values), 'application/json')}
        if new_file:
            files['file'] = (os.path.basename(new_file.name), new_file)

        response = requests.put(
            self.base_url + '/tasks/' + task_key,
            files=files
        )
        if response.status_code == HTTPStatus.OK:
            return Task.Schema().load(response.json())
        else:
            raise StatusError(response.json()['error'])

    def delete(self, task_key: str) -> Task:
        """
        Delete a task.

        The given task key can be either its ID or name.
        """

        if not bson.ObjectId.is_valid(task_key):
            response = requests.get(self.base_url + '/tasks?name=' + task_key)
            if response.status_code != HTTPStatus.OK:
                raise StatusError(response.json()['error'])
            task_key = response.json()['_id']

        response = requests.delete(self.base_url + '/tasks/' + task_key)
        if response.status_code == HTTPStatus.OK:
            return Task.Schema().load(response.json())
        else:
            raise StatusError(response.json()['error'])
