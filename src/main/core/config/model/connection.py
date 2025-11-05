from attr import dataclass, define

from main.core.ActonTypeEnum import DriverTypeEnum


@define
class Connection:
    name: str
    type: DriverTypeEnum
    connection_uri: str
    host: str
    port: int
    user: str
    password: str


    def __init__(self, values: dict):
        self.name = values['name']
        self.type = DriverTypeEnum.fromLabel(values['type'])
        self.connection_uri = values.get('connection_uri', '')
        self.host = values.get('host', '')
        self.port = values.get('port', '')
        self.user = values.get("user", '')
        self.password = values.get("password", '')

        if (not self.connection_uri and (not self.host or not self.port)):
            raise ValueError(f"Invalid connection configuration {self}")
