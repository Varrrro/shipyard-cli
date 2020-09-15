import unittest

from unittest import mock

from click.testing import CliRunner
from bson import ObjectId

from shipyard_cli.errors import StatusError
from shipyard_cli.config import Config
from shipyard_cli.node.model import Node
from shipyard_cli.task.model import Task
from shipyard_cli.crane.commands import crane


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
            'ssh_user': 'Test2',
        }
    ], many=True)
    test_tasks = Task.Schema().load([
        {
            '_id': ObjectId(),
            'name': 'Test1',
            'runtime': 1000,
            'deadline': 1000,
            'period': 1000
        },
        {
            '_id': ObjectId(),
            'name': 'Test2',
            'runtime': 1000,
            'deadline': 1000,
            'period': 1000
        }
    ], many=True)

    def __init__(self, server_url: str, server_port: str):
        pass

    def deploy_task(self, node_key: str, task_key: str):
        for node in self.test_nodes:
            if str(node._id) == node_key:
                for task in self.test_tasks:
                    if str(task._id) == task_key:
                        return
                raise StatusError('Task not found.')
        raise StatusError('Node not found.')

    def remove_task(self, node_key: str, task_key: str):
        for node in self.test_nodes:
            if str(node._id) == node_key:
                for task in self.test_tasks:
                    if str(task._id) == task_key:
                        return
                raise StatusError('Task not found.')
        raise StatusError('Node not found.')


@mock.patch('shipyard_cli.crane.commands.CraneService', MockService)
class TestCommands(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.runner = CliRunner()
        self.config = Config(server_url='test', server_port='test')

    def test_deploy(self):
        result = self.runner.invoke(
            crane,
            ['deploy', str(MockService.test_nodes[0]._id),
             str(MockService.test_tasks[0]._id)],
            obj=self.config
        )
        self.assertIn('Deployment succesful', result.output)

        result = self.runner.invoke(
            crane,
            ['deploy', str(ObjectId()), str(ObjectId())],
            obj=self.config
        )
        self.assertIn('Unable to deploy task to node', result.output)

    def test_rm(self):
        result = self.runner.invoke(
            crane,
            ['rm', str(MockService.test_nodes[0]._id),
             str(MockService.test_tasks[0]._id)],
            input='y',
            obj=self.config
        )
        self.assertIn(
            'The task was removed from the node correctly', result.output)

        result = self.runner.invoke(
            crane,
            ['rm', str(ObjectId()), str(ObjectId())],
            input='y',
            obj=self.config
        )
        self.assertIn('Unable to remove task from node', result.output)
