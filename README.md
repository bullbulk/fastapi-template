# OAIP backend project

* Set .env variable SECRET_KEY. You can generate random string of 32 hex symbols by running:

  ```shell
  openssl rand -hex 32
  ```
  OpenSSL can be found on Windows in `C:\Program Files\Git\usr\bin`


* Start the stack with Docker Compose:

  ```shell
  docker-compose up -d
  ```

* And for the further use (rebuild image with code changes):

  ```shell
  docker-compose up -d --build
  ```

* After building there will remain old unused images, which take space on disk and in images list. To remove them, run:

  ```shell
  docker image prune --force
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

## Command Line Interface

You can use CLI-script with references to the most used commands.

* First, install requirements

  ```shell
  pip install -r ./cli/requirements.txt
  ```
  
* If you are working on Unix, run script as regular Python program or as executable:
  ```shell
  python cli.py --help
  
  chmod +x cli.py
  ./cli.py --help
  ```
  
* On Windows, just run program as usual:
  ```shell
  python cli.py --help
  ```

## Access to pgAdmin

* Open http://localhost:5050 in web browser and login as `admin@oaip.com` with password `qwerty` (you can edit
  PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD in .env). It may take long after start of the image. 
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

To get inside the container with a `shell` session you can do this via "CLI" button in Docker Desktop.

The other way is run `exec` inside the running container:

```console
$ docker-compose exec {container_name} shell
```

You should see an output like:

```shell
root@7f2607af31c3:/backend#
```


## Deploy to a Docker Swarm mode cluster

There are 3 steps:

1. **Build** your app images
2. Optionally, **push** your custom images to a Docker Registry
3. **Deploy** your stack

---

Here are the steps in detail:

1. **Build your app images**

```shell
python cli.py build --prod
```

2. **Optionally, push your images to a Docker Registry**

**Note**: if the deployment Docker Swarm mode "cluster" has more than one server, you will have to push the images to a registry or build the images in each server, so that when each of the servers in your cluster tries to start the containers it can get the Docker images for them, pulling them from a Docker Registry or because it has them already built locally.


```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml push
```

3. **Deploy your stack**

* Set these environment variables:
  * `STACK_NAME=oaip-com`

```shell
python cli.py deploy
```

---

#### Deployment Technical Details

Building and pushing is done with the `docker-compose.yml` file, using the `docker-compose` command. The file `docker-compose.yml` uses the file `.env` with default environment variables. And the scripts set some additional environment variables as well.

The deployment requires using `docker stack` instead of `docker-swarm`, and it can't read environment variables or `.env` files. It was the first motivation of creating CLI with API, which provides `.env` support.

You can do the process by hand based on those same scripts if you wanted. The general structure is like this:

```bash
# Use the environment variables passed to this script, as TAG
# And re-create those variables as environment variables for the next command
TAG=${TAG?Variable not set} 
# The actual command that does the work: "docker-compose" or "docker compose"
docker-compose \
# Pass the file that should be used, setting explicitly docker-compose.yml avoids the
# default of also using docker-compose.override.yml
-f docker-compose.yml \
-f docker-compose.prod.yml \
# Use the docker-compose sub command named "config", it just uses the docker-compose.yml
# file passed to it and prints their combined contents
# Put those contents in a file "docker-stack.yml", with ">"
config > docker-stack.yml

# The previous only generated a docker-stack.yml file,
# but didn't do anything with it yet

# Now this command uses that same file to deploy it
docker stack deploy -c docker-stack.yml "${STACK_NAME?Variable not set}"
```

## Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker-compose`.

And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker-compose` to apply overrides on top of `docker-compose.yml`. Docker automatically read `docker-compose.override.yml`, if you don't specify config file in command

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker-compose` command.

It is all designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

### The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

### Development URLs

Development URLs, for local development.

Backend: http://localhost:5555/api/

Automatic Interactive Docs (Swagger UI): https://localhost:5555/docs

Automatic Alternative Docs (ReDoc): https://localhost:5555/redoc

PGAdmin: http://localhost:5050
