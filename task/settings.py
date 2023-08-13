import os
import configparser
from dataclasses import dataclass


CONFIG_PATH = os.getenv("CONFIG_PATH", None)


@dataclass
class Settings:
    service_host: str
    service_port: str
    auth_service_host: str
    auth_service_port: str
    database_path: str
    log_level: int
    log_turn_on_file_handler: bool
    log_filepath: str
    broker_host: str
    broker_port: str


def parse_config(filepath: str) -> Settings:
    config = configparser.ConfigParser()
    config.read(filepath)

    return Settings(
        service_host=config.get("SERVICE", "host"),
        service_port=config.getint("SERVICE", "port"),
        auth_service_host=config.get("AUTH_SERVICE", "host"),
        auth_service_port=config.getint("AUTH_SERVICE", "port"),
        database_path=config.get("Database", "path"),
        log_level=config.getint("LOGGER", "level"),
        log_turn_on_file_handler=config.getboolean("LOGGER", "turn_on_file_handler"),
        log_filepath=config.get("LOGGER", "filepath"),
        broker_host=config.get("Broker", "host"),
        broker_port=config.get("Broker", "port"),
    )


settings = parse_config(CONFIG_PATH)
