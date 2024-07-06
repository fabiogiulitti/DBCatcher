from attr import dataclass

from core.ActonTypeEnum import DriverTypeEnum


#@dataclass
class Connection:
    name: str
    type: DriverTypeEnum
    connectionURI: str
    user: str
    password: str


    def __init__(self, values: dict):
        self.name = values['name']
        self.type = DriverTypeEnum.from_value(values['type'])
        self.connectionURI = values['connectionURI']
        self.user = values.get("user", None)
        self.password = values.get("password", None)
