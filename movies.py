import click
import requests as req

import apikey

base_url: str = "http://www.omdbapi.com/"


@click.command()
@click.argument("title")
@click.option("-y", "--year", type=int, help="Release year of the movie.")
@click.option(
    "-p",
    "--plot",
    type=click.Choice(["short", "full"]),
    default="short",
    help="Plot length: (short|full)",
)
def movie_info(title: str, year: int, plot: str = "short") -> None:
    """
    Fetch information about a movie.
    """

    api_key: str = apikey.decrypt_key()

    params = {
        "t": title,
        "apikey": api_key,
        "plot": plot,
    }
    if year:
        params["y"] = year

    res = req.get(base_url, params)

    if res.status_code == 200:
        data = res.json()
        click.echo(data)
