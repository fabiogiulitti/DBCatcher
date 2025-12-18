from signal import Signals, signal
from PyQt6.QtGui import QStandardItem
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from attrs import define
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.treepath import Node
from main.widgets.model.tree_node import TreeNode


def createItem(parent, text, node: Node) -> QStandardItem:
    parent_data = parent.getUserData()
    item = TreeNode(text, parent)
    #item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
    
    data = {'levelTag' : node.nodeType
            ,'sessionID' : node.session
            ,'type' : parent_data['type']}
    if ('path' in parent_data):
        data['path'] = parent_data['path'] + [text]
    else:
        data['path'] = [text]
    item.setUserData(data)
    if not node.leaf:
        addLoadingItem(item)
    return item

def addLoadingItem(item):
    item.addItem(TreeNode('(LOADING...)'))

@define
class DBCSignals(QObject):
    connection_added = pyqtSignal(dict)
    status_notify  = pyqtSignal(str, str)
    table_loaded = pyqtSignal(AbstractDataResponse)
    show_detail = pyqtSignal(str, str)
    executeQueryRequested = pyqtSignal(dict)
    results_updated = pyqtSignal(AbstractDataResponse)


    def __init__(self):
        super().__init__()
