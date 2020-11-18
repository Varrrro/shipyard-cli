"""
The application's entrypoint.
"""

import click

from shipyard_cli.config import load_config
from shipyard_cli.crane.commands import crane
from shipyard_cli.node.commands import node
from shipyard_cli.task.commands import task


@click.group()
@click.pass_context
def cli(ctx):
    """An orchestrator for real-time tasks."""

    ctx.obj = load_config()


@cli.command()
@click.pass_obj
@click.argument('key', type=str)
@click.argument('value', type=str)
def config(config, key, value):
    """Change the configuration."""

    config.update(key, value)


cli.add_command(node)
cli.add_command(task)
cli.add_command(crane)
