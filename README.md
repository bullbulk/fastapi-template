# oaip backend project

# Built with [FastAPI Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* And for the further use (build after editing):

```bash
docker-compose up -d --build
```

Backend, JSON based web API based on OpenAPI: http://localhost:5555/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:5555/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost:5555/redoc

PostgreSQL external connect: http://localhost:5432

PGAdmin, PostgreSQL web administration: http://localhost:5050 (not working for now)

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for
the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```

## Backend local development, additional details

Open your editor at `./app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code
inside. That way, your editor will be able to find all the imports, etc.

Modify or add SQLAlchemy models in `./app/models/`, Pydantic schemas in `./app/schemas/`, API endpoints in `./app/api/`,
CRUD (Create, Read, Update, Delete) utils in `./app/crud/`. The easiest might be to copy the ones for Items (models,
endpoints, and CRUD utils) and update them to your needs.

Check the `api_guide.py` to learn the basics of API of this project

To get inside the container with a `bash` session you can start the stack with:

```console
$ docker-compose up -d
```

and then `exec` inside the running container:

```console
$ docker-compose exec app bash
```

You should see an output like:

```console
root@7f2607af31c3:/app#
```

### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "
node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time,
and each time the volume would be created in that new node before starting the service. As a result, it would look like
your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files
in your main backend service (for example, if those files were uploaded by your users, or if they were created by your
system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them
be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only
one) of your nodes.

### Development URLs

Development URLs, for local development.

Backend: http://localhost:5555/api/

Automatic Interactive Docs (Swagger UI): https://localhost:5555/docs

Automatic Alternative Docs (ReDoc): https://localhost:5555/redoc

PGAdmin: http://localhost:5050

## Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

You can check the variables used during generation in the file `cookiecutter-config-file.yml`.

You can generate the project again with the same configurations used the first time.

That would be useful if, for example, the project generator (`tiangolo/full-stack-fastapi-postgresql`) was updated and
you wanted to integrate or review the changes.

You could generate a new project with the same configurations as this one in a parallel directory. And compare the
differences between the two, without having to overwrite your current code but being able to use the same variables used
for your current project.

To achieve that, the generated project includes the file `cookiecutter-config-file.yml` with the current variables used.

You can use that file while generating a new project to reuse all those variables.

For example, run:

```console
$ cookiecutter --config-file ./cookiecutter-config-file.yml --output-dir ../project-copy https://github.com/tiangolo/full-stack-fastapi-postgresql
```

That will use the file `cookiecutter-config-file.yml` in the current directory (in this project) to generate a new
project inside a sibling directory `project-copy`.
