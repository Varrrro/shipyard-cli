"""
Custom click types for specific inputs.
"""

import json
import socket

import click


class IPaddress(click.ParamType):
    """An IPv4 address."""

    name = 'IP'

    def convert(self, value, param, ctx):
        try:
            socket.inet_aton(value)
            return value
        except socket.error:
            self.fail(f'{value!r} is not a valid IP address.', param, ctx)


class JSONdocument(click.ParamType):
    """A JSON document."""

    name = 'JSON'

    def convert(self, value, param, ctx):
        try:
            doc = json.loads(value)
            return doc
        except TypeError:
            self.fail(
                'Expected string for json deserialization, got'
                f'{value!r} of type {type(value).__name__}.',
                param,
                ctx
            )
        except json.JSONDecodeError as e:
            self.fail(
                'Unable to decode JSON, error at index '
                f'{e.pos} line {e.lineno} column {e.colno}.',
                param,
                ctx
            )
