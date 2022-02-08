#!/usr/bin/env python3

from cli_res.utils import has_project_changed

try:
    import click
    from python_on_whales import DockerClient, docker
except ModuleNotFoundError:
    raise RuntimeError(
        "Some modules are not installed. If you want to use CLI, install dependencies in ./cli_res/requirements.txt"
    )


@click.group()
def main():
    """
    CLI-wrapper for Docker
    """
    pass


@main.command()
def up():
    """
    Docker Compose create and start containers with overrode configuration.
    If project files were changed, images will rebuild.
    """

    if has_project_changed():
        docker.compose.up(
            detach=True, build=True
        )
    else:
        docker.compose.up(
            detach=True
        )


if __name__ == "__main__":
    main()
