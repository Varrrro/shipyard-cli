"""
Commands for task related operations.
"""

import click
from marshmallow import ValidationError
from shipyard_cli.task.model import Task
from shipyard_cli.task.service import TaskService
from shipyard_cli.types import JSONdocument


@click.group()
@click.pass_context
def task(ctx):
    """Manage tasks."""

    ctx.obj = TaskService(ctx.obj.server_url, ctx.obj.server_port)


@task.command()
@click.pass_obj
def ls(service):
    """List tasks."""

    try:
        tasks = service.get_all()
        row = '{:<28}' * 5
        click.echo(row.format('ID', 'NAME', 'RUNTIME', 'DEADLINE', 'PERIOD'))
        for task in tasks:
            click.echo(row.format(
                str(task._id),
                task.name,
                task.runtime,
                task.deadline,
                task.period
            ))
    except Exception as e:
        click.echo('Unable to show task list:\n' + str(e))


@task.command()
@click.pass_obj
@click.option('--device', type=str, multiple=True, help='A device needed for the task.')
@click.argument('name', type=str)
@click.argument('runtime', type=int)
@click.argument('deadline', type=int)
@click.argument('period', type=int)
@click.argument('file', type=click.File('rb'))
def add(service, device, name, runtime, deadline, period, file):
    """Add a new task."""

    try:
        task = Task.Schema().load({
            'name': name,
            'runtime': runtime,
            'deadline': deadline,
            'period': period,
        })
        task.devices = list(d for d in device)
        new_id = service.create(task, file)
        click.echo(f'Added new task with ID {new_id}')
    except Exception as e:
        click.echo('Unable to add new task:\n' + str(e))


@task.command()
@click.pass_obj
@click.option('--file', '-f', type=click.File('rb'), help='New tar.gz containing the task\'s sources.')
@click.argument('key', type=str)
@click.argument('values', type=JSONdocument())
def update(service, file, key, values):
    """
    Update a task's values.

    The task is identified by a given KEY, which can be either the task's ID or
    its name.
    """

    try:
        Task.Schema().load(values)
        service.update(key, values, file)
        click.echo('The task\'s values were updated correctly.')
    except ValidationError as e:
        click.echo('Unable to update the task\'s values:\n' + str(e.messages))
    except Exception as e:
        click.echo('Unable to update the task\'s values:\n' + str(e))


@task.command()
@click.pass_obj
@click.confirmation_option('-y', '--yes', prompt='Are you sure you want to remove the task?')
@click.argument('key', type=str)
def rm(service, key):
    """
    Remove a task.

    The task is identified by a given KEY, which can be either the task's ID or
    its name.
    """

    try:
        service.delete(key)
        click.echo('The task was removed correctly.')
    except Exception as e:
        click.echo('Unable to remove the task:\n' + str(e))
