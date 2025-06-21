from signal import Signals, signal
from PyQt6.QtGui import QStandardItem
from PyQt6.QtCore import pyqtSignal, QObject
from attrs import define
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.treepath import Node


def createItem(parentData: dict, text: str, node: Node) -> QStandardItem:
    item = QStandardItem(text)
    
    data = {'levelTag' : node.nodeType
            ,'sessionID' : node.session
            ,'type' : parentData['type']}
    if ('path' in parentData):
        data['path'] = parentData['path'] + [text]
    else:
        data['path'] = [text]
    item.setData(data)
    if not node.leaf:
        addLoadingItem(item)
    return item

def addLoadingItem(item):
    item.appendRow(QStandardItem('(LOADING...)'))

@define
class DBCSignals(QObject):
    status_notify  = pyqtSignal(str, str)
    table_loaded = pyqtSignal(AbstractDataResponse)
    show_detail = pyqtSignal(str, str)


    def __init__(self):
        super().__init__()
