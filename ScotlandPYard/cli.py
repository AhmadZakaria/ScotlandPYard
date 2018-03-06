# -*- coding: utf-8 -*-

"""Console script for ScotlandPYard."""

import click
import ScotlandPYard.ScotlandPYard as spy

@click.command()
def main(args=None):
    """Console script for ScotlandPYard."""
    # click.echo("Replace this message by putting your code into "
    #            "ScotlandPYard.cli.main")
    spy.main()


if __name__ == "__main__":
    main()
