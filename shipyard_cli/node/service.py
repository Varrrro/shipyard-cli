"""
Business logic for node related operations.
"""

from http import HTTPStatus
from typing import List

import bson
import requests
from shipyard_cli.errors import StatusError
from shipyard_cli.node.model import Node


class NodeService():
    """Service for node operations."""

    def __init__(self, url: str, port: str):
        self.base_url = url + ':' + port

    def get_all(self) -> List[Node]:
        """Obtain the list of nodes."""

        response = requests.get(self.base_url + '/nodes')
        if response.status_code == HTTPStatus.OK:
            return Node.Schema().load(response.json(), many=True)
        else:
            raise StatusError(response.json()['error'])

    def get_one(self, node_key: str) -> Node:
        """
        Obtain detailed information about a node.

        The given node key can be either its ID or name.
        """

        if bson.ObjectId.is_valid(node_key):
            uri = '/nodes/' + node_key
        else:
            uri = '/nodes?name=' + node_key
        response = requests.get(self.base_url + uri)
        if response.status_code == HTTPStatus.OK:
            return Node.Schema().load(response.json())
        else:
            raise StatusError(response.json()['error'])

    def create(self, node: Node, ssh_user: str, ssh_pass: str) -> str:
        """Create a new node."""

        response = requests.post(
            self.base_url + '/nodes',
            auth=(ssh_user, ssh_pass),
            json=Node.Schema(exclude=['_id', 'tasks']).dump(node)
        )
        if response.status_code == HTTPStatus.OK:
            return response.json()['_id']
        else:
            raise StatusError(response.json()['error'])

    def update(self, node_key: str, new_values: dict) -> Node:
        """
        Change the values of a node.

        The given node key can be either its ID or name.
        """

        if not bson.ObjectId.is_valid(node_key):
            response = requests.get(self.base_url + '/nodes?name=' + node_key)
            if response.status_code != HTTPStatus.OK:
                raise StatusError(response.json()['error'])
            node_key = response.json()['_id']

        response = requests.put(
            self.base_url + '/nodes/' + node_key,
            json=new_values
        )
        if response.status_code == HTTPStatus.OK:
            return Node.Schema().load(response.json())
        else:
            raise StatusError(response.json()['error'])

    def delete(self, node_key: str) -> Node:
        """
        Delete a node.

        The given node key can be either its ID or name.
        """

        if not bson.ObjectId.is_valid(node_key):
            response = requests.get(self.base_url + '/nodes?name=' + node_key)
            if response.status_code != HTTPStatus.OK:
                raise StatusError(response.json()['error'])
            node_key = response.json()['_id']

        response = requests.delete(self.base_url + '/nodes/' + node_key)
        if response.status_code == HTTPStatus.OK:
            return Node.Schema().load(response.json())
        else:
            raise StatusError(response.json()['error'])
