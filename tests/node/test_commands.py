import unittest
import json

from unittest import mock
from typing import List

from click.testing import CliRunner
from bson import ObjectId

from shipyard_cli.errors import StatusError
from shipyard_cli.config import Config
from shipyard_cli.node.commands import node
from shipyard_cli.node.model import Node


class MockService():

    test_nodes = Node.Schema().load([
        {
            '_id': ObjectId(),
            'name': 'Test1',
            'ip': '1.1.1.1',
            'ssh_user': 'Test1',
            'tasks': [
                {
                    '_id': ObjectId(),
                    'name': 'Test',
                    'runtime': 1000,
                    'deadline': 1000,
                    'period': 1000
                }
            ],
            'devices': [
                '/dev/test1',
                '/dev/test2'
            ]
        },
        {
            '_id': ObjectId(),
            'name': 'Test2',
            'ip': '2.2.2.2',
            'ssh_user': 'Test2'
        }
    ], many=True)

    def __init__(self, server_url: str, server_port: str):
        pass

    def get_all(self) -> List[Node]:
        return self.test_nodes

    def get_one(self, node_key: str) -> Node:
        for node in self.test_nodes:
            if str(node._id) == node_key:
                return node
        raise StatusError('Node not found.')

    def create(self, node: Node, ssh_user: str, ssh_pass: str) -> str:
        for test_node in self.test_nodes:
            if test_node.name == node.name:
                raise StatusError('Name already present.')
        return ObjectId()

    def update(self, node_key: str, new_values: dict) -> Node:
        for node in self.test_nodes:
            if str(node._id) == node_key:
                return Node.Schema().load(new_values)
        raise StatusError('Node not found.')

    def delete(self, node_key: str) -> Node:
        for node in self.test_nodes:
            if str(node._id) == node_key:
                return node
        raise StatusError('Node not found.')


@mock.patch('shipyard_cli.node.commands.NodeService', MockService)
class TestCommands(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.runner = CliRunner()
        self.config = Config(server_url='test', server_port='test')

    def test_ls(self):
        result = self.runner.invoke(node, ['ls'], obj=self.config)
        self.assertIn(str(MockService.test_nodes[0]._id), result.output)
        self.assertIn(str(MockService.test_nodes[1]._id), result.output)

        result = self.runner.invoke(node, ['ls', '--active'], obj=self.config)
        self.assertIn(str(MockService.test_nodes[0]._id), result.output)
        self.assertNotIn(str(MockService.test_nodes[1]._id), result.output)

    def test_inspect(self):
        result = self.runner.invoke(
            node,
            ['inspect', str(MockService.test_nodes[0]._id)],
            obj=self.config
        )
        self.assertIn(
            str(MockService.test_nodes[0].tasks[0]._id),
            result.output
        )

        result = self.runner.invoke(
            node,
            ['inspect', str(ObjectId())],
            obj=self.config
        )
        self.assertIn('Unable to show node details', result.output)

    def test_create(self):
        result = self.runner.invoke(
            node,
            ['add', 'New', '0.0.0.0', '4'],
            input='test\ntest\ntest',
            obj=self.config
        )
        self.assertIn('Added new node', result.output)

        result = self.runner.invoke(
            node,
            ['add', 'Test1', '0.0.0.0', '4'],
            input='test\ntest\ntest',
            obj=self.config
        )
        self.assertIn('Unable to add new node', result.output)

    def test_update(self):
        result = self.runner.invoke(
            node,
            ['update', str(MockService.test_nodes[0]._id),
             json.dumps({'cpu_arch': 'ARMv7'})],
            obj=self.config
        )
        self.assertIn(
            'The node\'s values were updated correctly',
            result.output
        )

        result = self.runner.invoke(
            node,
            ['update', str(MockService.test_nodes[0]._id),
             json.dumps({'error': 'error'})],
            obj=self.config
        )
        self.assertIn('Unable to update the node\'s values', result.output)

        result = self.runner.invoke(
            node,
            ['update', str(ObjectId()), json.dumps({})],
            obj=self.config
        )
        self.assertIn('Unable to update the node\'s values', result.output)

    def test_rm(self):
        result = self.runner.invoke(
            node,
            ['rm', str(MockService.test_nodes[0]._id)],
            input='y',
            obj=self.config
        )
        self.assertIn('The node was removed correctly', result.output)

        result = self.runner.invoke(
            node,
            ['rm', '-y', str(MockService.test_nodes[0]._id)],
            obj=self.config
        )
        self.assertIn('The node was removed correctly', result.output)

        result = self.runner.invoke(
            node,
            ['rm', str(ObjectId())],
            input='y',
            obj=self.config
        )
        self.assertIn('Unable to remove the node', result.output)

        result = self.runner.invoke(
            node,
            ['rm', '-y', str(ObjectId())],
            obj=self.config
        )
        self.assertIn('Unable to remove the node', result.output)
