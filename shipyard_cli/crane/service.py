"""
Business logic for the orchestration operations.
"""

from http import HTTPStatus

import bson
import requests
from shipyard_cli.errors import StatusError


class CraneService():
    """Service for orchestration operations."""

    def __init__(self, url: str, port: str):
        self.base_url = url + ':' + port

    def __check_key(self, key: str, resource: str) -> str:
        """
        Check if the given key is a valid `ObjectId`.

        If it is not, this method considers its the name of a resource of the
        given type and retrieves its ID from the server.

        Returns the resource's ID as a string.
        """

        if bson.ObjectId.is_valid(key):
            return key
        response = requests.get(self.base_url + f'/{resource}s?name=' + key)
        if response.status_code == HTTPStatus.OK:
            return response.json()['_id']
        else:
            raise StatusError(response.json()['error'])

    def deploy_task(self, node_key: str, task_key: str):
        """
        Deploy a task to a node.

        The given keys can be either the resource names or their IDs.
        """

        node_key = self.__check_key(node_key, 'node')
        task_key = self.__check_key(task_key, 'task')

        response = requests.post(
            self.base_url + '/nodes/' + node_key + '/tasks?task_id=' + task_key
        )
        if response.status_code == HTTPStatus.OK:
            return
        else:
            raise StatusError(response.json()['error'])

    def remove_task(self, node_key: str, task_key: str):
        """
        Remove a task from a node.

        The given keys can be either the resource names or their IDs.
        """

        node_key = self.__check_key(node_key, 'node')
        task_key = self.__check_key(task_key, 'task')

        response = requests.delete(
            self.base_url + '/nodes/' + node_key + '/tasks/' + task_key
        )
        if response.status_code == HTTPStatus.OK:
            return
        else:
            raise StatusError(response.json()['error'])
