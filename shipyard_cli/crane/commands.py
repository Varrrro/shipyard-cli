"""
Commands for the orchestration operations.
"""

import click
from shipyard_cli.crane.service import CraneService


@click.group()
@click.pass_context
def crane(ctx):
    """Manage task deployment."""

    ctx.obj = CraneService(ctx.obj.server_url, ctx.obj.server_port)


@crane.command()
@click.pass_obj
@click.argument('node', type=str)
@click.argument('task', type=str)
def deploy(service, node, task):
    """
    Deploy task to node.

    The NODE and TASK arguments are the keys to each resource respectively.
    These keys can be their IDs or their names.
    """

    try:
        service.deploy_task(node, task)
        click.echo('Deployment succesful.')
    except Exception as e:
        click.echo('Unable to deploy task to node:\n' + str(e))


@crane.command()
@click.pass_obj
@click.confirmation_option('-y', '--yes', prompt='Are you sure you want to remove the task from the node?')
@click.argument('node', type=str)
@click.argument('task', type=str)
def rm(service, node, task):
    """
    Remove task from node.

    The NODE and TASK arguments are the keys to each resource respectively.
    These keys can be their IDs or their names.
    """

    try:
        service.remove_task(node, task)
        click.echo('The task was removed from the node correctly.')
    except Exception as e:
        click.echo('Unable to remove task from node:\n' + str(e))
