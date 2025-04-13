from main import cli_args
from main.core.config.configyaml import ConfigManager
from main.core.config.model.connection import Connection


def retrieveConnections() -> list:
    
    config = ConfigManager(cli_args.config_file)
    try:
        values = config.get_value("connections")
        connections = []
        if isinstance(values, list):
            for value in values:
                connections.append(Connection(value))
        else:
            print("Malformed connections field")
    except ConnectionResetError as e:
        print(f"error {e}")
    return connections
