from PyQt6.QtGui import QStandardItem
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