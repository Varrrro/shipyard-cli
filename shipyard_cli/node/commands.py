"""
Commands for node related operations.
"""

import click
from marshmallow import ValidationError
from shipyard_cli.errors import StatusError
from shipyard_cli.node.model import Node
from shipyard_cli.node.service import NodeService
from shipyard_cli.types import IPaddress, JSONdocument


@click.group()
@click.pass_context
def node(ctx):
    """Manage nodes."""

    ctx.obj = NodeService(ctx.obj.server_url, ctx.obj.server_port)


@node.command()
@click.pass_obj
@click.option('--active', is_flag=True, help='Only show the nodes that are currently running tasks.')
def ls(service, active):
    """List nodes."""

    try:
        nodes = service.get_all()
        row = '{:<28}' * 4
        click.echo(row.format('ID', 'NAME', 'ADDRESS', 'TASKS'))
        for node in nodes:
            if active and len(node.tasks) == 0:
                continue
            click.echo(row.format(
                str(node._id),
                node.name,
                node.ip,
                len(node.tasks)
            ))
    except Exception as e:
        click.echo('Unable to show node list:\n' + str(e))


@node.command()
@click.pass_obj
@click.argument('key', type=str)
def inspect(service, key):
    """
    Show detailed information about a node.

    The node is identified by a given KEY, which can be either the node's ID or
    its name.
    """

    try:
        node = service.get_one(key)
        row = '{:<28}' * 5
        click.echo(row.format('TASK ID',
                              'NAME',
                              'RUNTIME',
                              'DEADLINE',
                              'PERIOD'
                              ))
        for task in node.tasks:
            click.echo(row.format(str(task._id),
                                  task.name,
                                  task.runtime,
                                  task.deadline,
                                  task.period
                                  ))
    except Exception as e:
        click.echo('Unable to show node details:\n' + str(e))


@node.command()
@click.pass_obj
@click.option('--cpu', type=str, help='The node\'s CPU model.')
@click.option('--cpu-arch', type=str, help='The node\'s CPU architecture.')
@click.option('--cpu-freq', type=int, help='The node\'s CPU frequency in MHz.')
@click.option('--ram', type=int, help='The node\'s RAM capacity.')
@click.option('--device', type=str, multiple=True, help='A device present in the node.')
@click.argument('name', type=str)
@click.argument('address', type=IPaddress())
@click.argument('cpu-cores', type=int)
def add(service, name, address, cpu_cores, cpu, cpu_arch, cpu_freq, ram, device):
    """Add a new node."""

    ssh_user = click.prompt('User', type=str)
    ssh_pass = click.prompt('Password', type=str,
                            hide_input=True, confirmation_prompt=True)
    try:
        node = Node.Schema().load({
            'name': name,
            'ip': address,
            'cpu': cpu,
            'cpu_arch': cpu_arch,
            'cpu_cores': cpu_cores,
            'cpu_freq': cpu_freq,
            'ram': ram,
        })
        node.devices = list(d for d in device)
        new_id = service.create(node, ssh_user, ssh_pass)
        click.echo(f'Added new node with ID {new_id}.')
    except Exception as e:
        click.echo('Unable to add new node:\n' + str(e))


@node.command()
@click.pass_obj
@click.argument('key', type=str)
@click.argument('values', type=JSONdocument())
def update(service, key, values):
    """
    Update a node's values.

    The node is identified by a given KEY, which can be either the node's ID or
    its name.

    The new VALUES must be specified as JSON.
    """

    try:
        Node.Schema().load(values)
        service.update(key, values)
        click.echo('The node\'s values were updated correctly.')
    except ValidationError as e:
        click.echo('Unable to update the node\'s values:\n' + str(e.messages))
    except Exception as e:
        click.echo('Unable to update the node\'s values:\n' + str(e))


@node.command()
@click.pass_obj
@click.confirmation_option('-y', '--yes', prompt='Are you sure you want to remove the node?')
@click.argument('key', type=str)
def rm(service, key):
    """
    Remove a node.

    The node is identified by a given KEY, which can be either the node's ID or
    its name.
    """

    try:
        service.delete(key)
        click.echo('The node was removed correctly.')
    except Exception as e:
        click.echo('Unable to remove the node:\n' + str(e))
