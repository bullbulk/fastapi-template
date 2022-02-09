#!/usr/bin/env python3

from cli_res.utils import has_project_changed, ENV_PATH, COMPOSE_FILE, STACK_NAME, COMPOSE_PROD_FILE

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
@click.option(
    '-p', '--prod',
    is_flag=True,
    default=False,
    help="Build containers with TAG set to \":prod\" and network configured for deployment."
)
def build(prod):
    """
    Build Docker images.
    """

    compose_files = [COMPOSE_FILE]
    if prod:
        compose_files.append(COMPOSE_PROD_FILE)
    client = DockerClient(compose_files=compose_files)
    client.compose.build()


@main.command()
def up():
    """
    Docker Compose create and start containers with override configuration.
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


@main.command()
@click.pass_context
def deploy(ctx: click.Context):
    """
    Create Docker Swarm stack with prebuilt images.
    """

    ctx.invoke(build, prod=True)
    stack = docker.stack.deploy(
        STACK_NAME,
        compose_files=[COMPOSE_FILE, COMPOSE_PROD_FILE],
        env_files=[ENV_PATH],
        prune=True,
        variables={'TAG': "prod"},
    )


@main.command()
@click.pass_context
def recreate(ctx: click.Context):
    """
    Recreate Compose stack including volumes.
    """

    ctx.invoke(down, volumes=True)
    up()


@main.command()
@click.option(
    '-v', '--volumes',
    is_flag=True,
    default=False,
    help="Remove named volumes declared in the volumes section of "
         "the Compose file and anonymous volumes "
         "attached to containers."
)
def down(volumes):
    """
    Delete Compose stack.
    """

    docker.compose.down(volumes=volumes)


@main.command()
def stop():
    """
    Stop Compose stack without waiting
    """
    docker.compose.stop(timeout=0)


if __name__ == "__main__":
    main()
