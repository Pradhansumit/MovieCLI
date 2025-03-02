import click

import apikey
import movies


@click.group()
def cli():
    pass


cli.add_command(apikey.add_apikey)
cli.add_command(movies.movie_info)
