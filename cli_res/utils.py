from pathlib import Path

import checksumdir
from appdirs import user_data_dir
from dotenv import get_key
from lightdb import LightDB

ENV_PATH = ".env"
COMPOSE_FILE = "docker-compose.yml"
COMPOSE_PROD_FILE = "docker-compose.prod.yml"
CONFIG_FILENAME = "config.json"
STACK_NAME = get_key(ENV_PATH, "STACK_NAME")
PROJECT_NAME = get_key(ENV_PATH, "PROJECT_NAME")


def get_config_path() -> Path:
    config_dir = Path(user_data_dir(PROJECT_NAME))

    if not config_dir.exists():
        config_dir.mkdir(parents=True)

    return config_dir.joinpath(CONFIG_FILENAME)


db = LightDB(str(get_config_path()))


def get_db() -> LightDB:
    return db


def get_checksum() -> str:
    return checksumdir.dirhash(".")


def get_stored_checksum() -> str | None:
    return db.get("checksum")


def set_project_checksum() -> str:
    checksum = get_checksum()
    db.set("checksum", get_checksum())
    return checksum


def has_project_changed() -> bool:
    stored_checksum = get_stored_checksum()
    changed = get_checksum() != stored_checksum
    if not stored_checksum or changed:
        set_project_checksum()
    return changed
