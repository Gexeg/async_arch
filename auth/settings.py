import configparser
from dataclasses import dataclass


CONFIG_PATH = "/app/config/local.ini"


@dataclass
class Settings:
    database_path: str
    jwt_secret: str
    jwt_expiration_time: int


def parse_config(filepath: str) -> Settings:
    config = configparser.ConfigParser()
    config.read(filepath)

    database_section = config["Database"]
    jwt_section = config["JWT"]

    return Settings(
        database_path=database_section["path"],
        jwt_secret=jwt_section["secret"],
        jwt_expiration_time=int(jwt_section["expiration_time"])
    )


settings = parse_config(CONFIG_PATH)
