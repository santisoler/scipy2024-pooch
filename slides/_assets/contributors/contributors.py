#!/usr/bin/env python
import requests
import click

BASE_URL = "https://github.com"
IGNORE = ["dependabot[bot]", "fatiando-bot"]


def get_contributors(
    organization,
    repository,
    github_username=None,
    github_token=None,
    contributors_per_page=1000,
):
    if not isinstance(contributors_per_page, int):
        raise ValueError(
            f"Invalid 'contributors_per_page' of type {type(contributors_per_page)}."
            "It must be an int."
        )
    url = (
        "https://api.github.com/repos/"
        f"{organization}/"
        f"{repository}/"
        f"contributors?per_page={contributors_per_page}"
    )
    auth = None
    if github_username is not None and github_token is not None:
        auth = (github_username, github_token)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    contributors = [entry["login"] for entry in response.json()]
    return contributors


def download(url):
    response = requests.get(url)
    response.raise_for_status()
    fname = url.split("/")[-1]
    with open(fname, "wb") as f:
        f.write(response.content)


@click.command
@click.argument("organization")
@click.argument("repo")
def cli(organization, repo):
    contributors = [c for c in get_contributors(organization, repo) if c not in IGNORE]
    for contributor in contributors:
        download(f"{BASE_URL}/{contributor}.png")


if __name__ == "__main__":
    cli()
