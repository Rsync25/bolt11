""" bolt11 CLI """

import json
import sys
from typing import Optional

import click

from .decode import decode as bolt11_decode
from .encode import encode as bolt11_encode
from .exceptions import Bolt11Exception
from .types import Bolt11

# disable tracebacks on exceptions
sys.tracebacklimit = 0


@click.group()
def command_group():
    """
    Python CLI for BOLT11 invoices
    decode bolt11 invoices
    """


@click.command()
@click.argument("bolt11", type=str)
@click.argument("ignore_exceptions", type=bool, default=True)
@click.argument("strict", type=bool, default=False)
def decode(bolt11, ignore_exceptions, strict):
    """
    decode a bolt11 invoice
    """
    decoded = bolt11_decode(bolt11, ignore_exceptions=ignore_exceptions, strict=strict)
    click.echo(decoded.json)


@click.command()
@click.argument("json_string", type=str)
@click.argument("private_key", type=str, default=None, required=False)
@click.argument("ignore_exceptions", type=bool, default=True)
@click.argument("strict", type=bool, default=False)
def encode(
    json_string,
    ignore_exceptions: bool = True,
    strict: bool = False,
    private_key: Optional[str] = None,
):
    """
    encode a bolt11 invoice
    EXAMPLE:
    {
        "currency": "bc",
        "amount_msat": 1000,
        "date": 1590000000,
        "tags": {
            "d": "description"
        }
    }
    private_key: e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734
    """
    try:
        data = json.loads(json_string)
    except json.decoder.JSONDecodeError:
        click.echo("invalid json")
        return

    try:
        encoded = bolt11_encode(
            Bolt11(**data),
            private_key,
            ignore_exceptions=ignore_exceptions,
            strict=strict,
        )
        click.echo(encoded)
    except Bolt11Exception as exc:
        click.echo(str(exc))


def main():
    """main function"""
    command_group.add_command(decode)
    command_group.add_command(encode)
    command_group()


if __name__ == "__main__":
    main()
