import socket
import json

import click


class IPaddress(click.ParamType):
    name = 'IP'

    def convert(self, value, param, ctx):
        try:
            socket.inet_aton(value)
            return value
        except socket.error:
            self.fail(f'{value!r} is not a valid IP address.', param, ctx)


class JSONdocument(click.ParamType):
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
