#!/usr/bin/env python3
# Copyright 2022 Matthew Karas
import click
import requests
import yaml
from requests.structures import CaseInsensitiveDict
from yaml import Loader

BASE_URL = "https://api.digitalocean.com/v2"


@click.group()
@click.pass_context
def cli(ctx):
    """
    Set up the context to have a headers item that will help make requests
    """
    ctx.ensure_object(dict)
    with open("config.yaml", "r") as fid:
        ctx.obj["config"] = yaml.load(fid.read(), Loader=Loader)
        if "default" in ctx.obj["config"]["auth-contexts"]:
            token = ctx.obj["config"]["auth-contexts"]["default"]
            ctx.obj["token"] = token
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/json"
            headers["Authorization"] = f"Bearer {token}"
            ctx.obj["headers"] = headers


@cli.command()
@click.pass_context
def account(ctx):
    url = f"{BASE_URL}/account"
    print(url)
    response = requests.get(url, headers=ctx.obj["headers"])
    print(response.json())


@cli.command()
@click.argument("token")
@click.option("--context", type=click.STRING, default="default")
@click.pass_context
def init(ctx, token, context):
    with open("config.yaml", "w") as fid:
        config = {"auth-contexts": {context: token}}
        yaml.dump(config, fid)


if __name__ == "__main__":
    cli()
