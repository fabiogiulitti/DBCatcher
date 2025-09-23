from abc import ABC, abstractmethod
import logging
from textwrap import wrap
import threading
from tokenize import StopTokenizing
from typing import Any, Callable, Generic, Type, TypeVar
from venv import logger


logging.basicConfig(
    filename='dbcatcher.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(filename)s] - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z'
)


T = TypeVar("T")
class AbstractConnectionStrategy(ABC, Generic[T]):
    timeout = 15 #minutes

#    @abstractmethod
    @staticmethod
    def connect(params: dict[str, str]):
        pass

    @abstractmethod
    def isConnected(conn: Any):
        pass

    @abstractmethod
    def close(self: T):
        pass

class DBCTimer(threading.Timer):

    def __init__(self, interval: float, function: Callable[..., object], args = None, kwargs = None) -> None:
        super().__init__(interval, function, args, kwargs)
        self._query_in_progress: threading.Event

    def run(self):
            while True:
                self.finished.wait(self.interval)
                if not self.finished.is_set() and self._query_in_progress.is_set():
                    self.function(*self.args, **self.kwargs)
                    break
                self.finished.clear()
            self.finished.set()


    def reset(self):
        self.finished.set()


class ConnectionProxy():

    def __init__(self, strategy: Type[AbstractConnectionStrategy], connection_uri=None, db_name=None, **kvargs) -> None:
        self._strategy: Type[AbstractConnectionStrategy] = strategy
        if connection_uri:
            self._params = {'connection_uri' : connection_uri, 'db_name' : db_name}
            self._conn  = self._strategy.connect(self._params)
        else:
            self._params = {'host' : kvargs['host'], 'port' : kvargs['port']}
            self._conn  = self._strategy.connect(self._params)
        self._query_in_progress = threading.Event()
        self._query_in_progress.set()
        self.initializeTimer()

    def initializeTimer(self):
        self._timer = DBCTimer(60 * 2, self.close)
        self._timer.daemon = True
        self._timer._query_in_progress = self._query_in_progress
        self._timer.start()
        logger.debug(f"Initialized timer of {2} minutes")


    def __getattr__(self, name: str) -> Any:
        if hasattr(self._conn, name):
            if not self._strategy.isConnected(self._conn):
                self._conn = self._strategy.connect(self._params)
                logging.debug(f"Auto reconnect {self._params}")
                self.initializeTimer()
            
            attr = getattr(self._conn, name)
            def wrapFunction(*args, **kvargs):
                if not self._query_in_progress.is_set():
                    raise RuntimeError("An other query is still running. Please wait until it is complete or cancel it")
                self._query_in_progress.clear()
                result = attr(*args, **kvargs)
                self._timer.reset()
                self._query_in_progress.set()
                return result

            return wrapFunction
        else:
            raise AttributeError(f"Object {object} has no attribute {name}")


    def close(self):
        logging.debug(f"Close unused connection {self._params}")
        self._strategy.close(self._conn)

