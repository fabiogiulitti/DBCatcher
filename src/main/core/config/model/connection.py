from attr import dataclass

from main.core.ActonTypeEnum import DriverTypeEnum


#@dataclass
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

        if (self.connection_uri is None and (self.host is None or self.port is None)):
            print("Invalid configuration {self}")
