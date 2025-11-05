import logging
from typing import Optional

from main import cli_args
from main.core.config.configyaml import ConfigManager
from main.core.config.model.connection import Connection


def retrieveConnection(name: str) -> Optional[Connection]:
    config = ConfigManager(cli_args.config_file)
    try:
        values = config.get_value("connections")
        connections = []
        if isinstance(values, list):
            for value in values:
                if value['name'] == name:
                    return Connection(value)
    except ConnectionResetError as e:
        logging.error(f"Connection not found {e}")
        raise e


def retrieveConnections() -> list:
    
    config = ConfigManager(cli_args.config_file)
    try:
        values = config.get_value("connections")
        connections = []
        if isinstance(values, list):
            for value in values:
                connections.append( Connection(value))
    except ConnectionResetError as e:
        print(f"error {e}")
    return connections

def addConnection(con_dict: dict) -> None:
    config = ConfigManager(cli_args.config_file)
    try:
        values: list = config.get_value("connections")
        if not values: values = []
        if any(con_dict['name'] == x['name'] for x in values): raise ValueError(f"Connection {con_dict['name']} is already defined")
        values.append(con_dict)
        config.set_value("connections", values)
    except Exception as e:
        logging.error(f"invalit configuration item {values}")
        raise e


def updateConnection(conn_dict: dict) -> None:
    config = ConfigManager(cli_args.config_file)
    try:
        values: list = config.get_value("connections")
        if not values: raise Exception(f"No connections defined")
        conn_index = next((i for i,v in enumerate(values) if v['name'] == conn_dict['name'])) #, (_ for _ in ()).throw(ValueError("Elemento non trovato")))
        values[conn_index] = conn_dict
        config.set_value("connections", values)
    except Exception as e:
        logging.error(f"invalit configuration item {values}")
        raise e
