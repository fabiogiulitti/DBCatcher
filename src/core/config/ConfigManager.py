from ast import List
from core.config.configyaml import config as conf
from core.config.model.connection import Connection

def retrieveConnections() -> list:
    try:
        values = conf.get_value("connections")
        connections = []
        if isinstance(values, list):
            for value in values:
                connections.append(Connection(value))
        else:
            print("Malformed connections field")
    except ConnectionResetError as e:
        print(f"error {e}")
    return connections
