# Copyright 2022 Matthew Karas
import click
import yaml


@click.group()
def cli():
    pass


@click.argument("token")
@click.option("context", type=click.STRING, default="default")
def init(token, context):
    with open("config.yaml", "w") as fid:
        config = {"auth-contexts": {context: token}}
        yaml.dump(config, fid)


if __name__ == "__main__":
    cli()
