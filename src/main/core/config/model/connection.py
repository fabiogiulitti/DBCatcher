from attr import dataclass

from core.ActonTypeEnum import DriverTypeEnum


#@dataclass
class Connection:
    name: str
    type: DriverTypeEnum
    connectionURI: str
    host: str
    port: int
    user: str
    password: str


    def __init__(self, values: dict):
        self.name = values['name']
        self.type = DriverTypeEnum.fromLabel(values['type'])
        self.connectionURI = values.get('connectionURI', None)
        self.host = values.get('host', None)
        self.port = values.get('port', None)
        self.user = values.get("user", None)
        self.password = values.get("password", None)

        if (self.connectionURI is None and (self.host is None or self.port is None)):
            print("Invalid configuration {self}")
