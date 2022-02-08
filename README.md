# OAIP backend project

* Set .env variable SECRET_KEY. You can generate random string of 32 hex symbols by running (openssl can be found on
  Windows in `C:\Program Files\Git\usr\bin`:

  ```shell
  openssl rand -hex 32
  ```

* Start the stack with Docker Compose:

  ```shell
  docker-compose up -d
  ```

* And for the further use (build after editing):

  ```shell
  docker-compose up -d --build
  ```

* Or you can use CLI-script by running:

  ```shell
  pip install -r ./cli/requirements.txt
  ```
  
* Next, on Unix:
  ```shell
  chmod +x cli.py
  ./cli.py up
  ```
  
  Windows:
  ```shell
  python cli.py up
  ```

* After building there will remain old unused images, which take space on disk and in images list. To remove them, run:

  ```shell
  docker image prune
  ```

Backend, JSON based web API based on OpenAPI: http://localhost:5555/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:5555/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost:5555/redoc

PostgreSQL external connect: http://localhost:5432

PGAdmin, PostgreSQL web administration: http://localhost:5050

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for
the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```shell
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```shell
docker-compose logs backend
```

## Access to pgAdmin

* Open http://localhost:5050 in web browser and login as `admin@oaip.com` with password `qwerty` (you can edit
  PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD in .env)
* Create new server: in `General` enter any name, go to `Connection` and set next options:
    * Host name/address: `postgres`
    * Port: `5432`
    * Username: `admin` (POSTGRES_USER)
    * Password: `qwerty` (POSTGRES_PASSWORD)

## Backend local development, additional details

Open your editor at `./app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code
inside. That way, your editor will be able to find all the imports, etc.

Modify or add SQLAlchemy models in `./app/models/`, Pydantic schemas in `./app/schemas/`, API endpoints in `./app/api/`,
CRUD (Create, Read, Update, Delete) utils in `./app/crud/`. The easiest might be to copy the ones for Items (models,
endpoints, and CRUD utils) and update them to your needs.

Check the `api_guide.py` to learn the basics of API of this project

To get inside the container with a `shell` session you can start the stack with:

```console
$ docker-compose up -d
```

and then `exec` inside the running container:

```console
$ docker-compose exec app shell
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
