from abc import ABC, abstractmethod
from enum import Enum


class FetchTypeEnum(Enum):
    DOWNLOAD = 1
    VIEW     = 2


class AbstractBigColumnFetchInfo(ABC):

    @property
    @abstractmethod
    def fetch_type(self) -> FetchTypeEnum:
        ...

    @property
    @abstractmethod
    def type(self):
        ...

    @property
    @abstractmethod
    def object(self):
        ...

    @property
    @abstractmethod
    def length(self) -> int:
        ...

    @abstractmethod
    def read(self, offset: int, chunk_size: int) -> bytes:
        ...
