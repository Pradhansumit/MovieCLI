import os

import click
import requests as req

import apikey

BASE_URL: str = "http://www.omdbapi.com/"
EXPORT_PATH: str = os.path.join(apikey.ROOT_FOLDER, "file-history.csv")


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
@click.option(
    "-e",
    "--export",
    type=click.Choice(["true", "false"]),
    default="false",
    help="To export data",
)
def info(title: str, year: int, plot: str = "short", export: str = "false") -> None:
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

    res = req.get(BASE_URL, params)

    if res.status_code == 200:
        data = res.json()
        # formated data
        type = data.get("Type")
        if type == "movie":
            formatted_data = f"""
            {{
            🎬 Title: {data.get("Title")},
            🗓️ Year: {data.get("Released")},
            🎥 Plot: {data.get("Plot")},
            🎭 Genre: {data.get("Genre")},
            😎 Actors: {data.get("Actors")},
            🧐 Director: {data.get("Director")},
            🍿 Type: {data.get("Type")}
            }}'
            """
        else:
            formatted_data = f"""
            {{
            🎬 Title: {data.get("Title")},
            🗓️ Year: {data.get("Released")},
            🎥 Plot: {data.get("Plot")},
            🎭 Genre: {data.get("Genre")},
            😎 Actors: {data.get("Actors")},
            🧐 Director: {data.get("Director")},
            📺 Type: {data.get("Type")},
            🐽 Seasons: {data.get("totalSeasons")}
            }}'
            """

        click.echo(formatted_data)

        if export == "true":
            import csv

            with open(EXPORT_PATH, "a") as expFile:
                csv_writer = csv.writer(expFile)

                if os.path.isfile(EXPORT_PATH):
                    csv_writer.writerow(
                        [
                            "Title",
                            "Year",
                            "Plot",
                            "Genre",
                            "Actors",
                            "Director",
                            "Type",
                            "Seasons",
                        ]
                    )
                if data.get("Type") == "movie":
                    csv_writer.writerow(
                        [
                            data.get("Title"),
                            data.get("Released"),
                            data.get("Plot"),
                            data.get("Genre"),
                            data.get("Actors"),
                            data.get("Director"),
                            data.get("Type"),
                            "NA",
                        ]
                    )
                else:
                    csv_writer.writerow(
                        [
                            data.get("Title"),
                            data.get("Released"),
                            data.get("Plot"),
                            data.get("Genre"),
                            data.get("Actors"),
                            data.get("Director"),
                            data.get("Type"),
                            data.get("totalSeasons"),
                        ]
                    )

    elif res.status_code == 401:
        raise Exception("🥷 You're not authorized.")
    else:
        raise Exception(f"Throwing error from request, {res.status_code}")
