import unittest
import io
import json

from typing import List
from unittest import mock

from click.testing import CliRunner
from bson import ObjectId

from shipyard_cli.errors import StatusError
from shipyard_cli.config import Config
from shipyard_cli.task.commands import task
from shipyard_cli.task.model import Task


class MockService():

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

    def get_all(self) -> List[Task]:
        return self.test_tasks

    def get_one(self, task_key: str) -> Task:
        for task in self.test_tasks:
            if str(task._id) == task_key:
                return task
        raise StatusError('Task not found.')

    def create(self, task: Task, file: io.BufferedReader) -> str:
        for test_task in self.test_tasks:
            if test_task.name == task.name:
                raise StatusError('Name already present.')
        return ObjectId()

    def update(self, task_key: str, new_values: dict, new_file: io.BufferedReader) -> Task:
        for task in self.test_tasks:
            if str(task._id) == task_key:
                return Task.Schema().load(new_values)
        raise StatusError('Task not found.')

    def delete(self, task_key: str) -> Task:
        for task in self.test_tasks:
            if str(task._id) == task_key:
                return task
        raise StatusError('Task not found.')


@mock.patch('shipyard_cli.task.commands.TaskService', MockService)
class TestCommands(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.runner = CliRunner()
        self.config = Config(server_url='test', server_port='test')

    def test_ls(self):
        result = self.runner.invoke(
            task,
            ['ls'],
            obj=self.config
        )
        self.assertIn(str(MockService.test_tasks[0]._id), result.output)
        self.assertIn(str(MockService.test_tasks[1]._id), result.output)

    def test_add(self):
        with self.runner.isolated_filesystem():
            with open('test.tar.gz', 'wb') as f:
                f.write(str.encode('Test'))

            result = self.runner.invoke(
                task,
                ['add', 'Test', '1000', '1000', '1000', 'test.tar.gz'],
                obj=self.config
            )
            self.assertIn('Added new task', result.output)

            result = self.runner.invoke(
                task,
                ['add', '--device', '/dev/null', 'Test',
                    '1000', '1000', '1000', 'test.tar.gz'],
                obj=self.config
            )
            self.assertIn('Added new task', result.output)

            result = self.runner.invoke(
                task,
                ['add', 'Test1', '1000', '1000', '1000', 'test.tar.gz'],
                obj=self.config
            )
            self.assertIn('Unable to add new task', result.output)

    def test_update(self):
        with self.runner.isolated_filesystem():
            with open('test.tar.gz', 'wb') as f:
                f.write(str.encode('Test'))

            result = self.runner.invoke(
                task,
                ['update', str(MockService.test_tasks[0]._id),
                 json.dumps({'runtime': 10})],
                obj=self.config
            )
            self.assertIn(
                'The task\'s values were updated correctly',
                result.output
            )

            result = self.runner.invoke(
                task,
                ['update', '-f', 'test.tar.gz',
                    str(MockService.test_tasks[0]._id), json.dumps({'runtime': 10})],
                obj=self.config
            )
            self.assertIn(
                'The task\'s values were updated correctly',
                result.output
            )

            result = self.runner.invoke(
                task,
                ['update', str(ObjectId()), json.dumps({'runtime': 10})],
                obj=self.config
            )
            self.assertIn(
                'Unable to update the task\'s values',
                result.output
            )

    def test_rm(self):
        result = self.runner.invoke(
            task,
            ['rm', str(MockService.test_tasks[0]._id)],
            input='y',
            obj=self.config
        )
        self.assertIn('The task was removed correctly', result.output)

        result = self.runner.invoke(
            task,
            ['rm', '-y', str(MockService.test_tasks[0]._id)],
            obj=self.config
        )
        self.assertIn('The task was removed correctly', result.output)

        result = self.runner.invoke(
            task,
            ['rm', str(ObjectId())],
            input='y',
            obj=self.config
        )
        self.assertIn('Unable to remove the task', result.output)

        result = self.runner.invoke(
            task,
            ['rm', '-y', str(ObjectId())],
            obj=self.config
        )
        self.assertIn('Unable to remove the task', result.output)
