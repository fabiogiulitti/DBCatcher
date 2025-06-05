from attr import ib, s
from main.core.driver.abstractdataresponse import AbstractDataResponse
from main.core.treepath import TreePath,make_session_id, references
from main.core.treepath import ItemAction
from pymongo import MongoClient
from pymongo.collection import Collection
from json import dumps
from main.widgets.ContentData import ContentData, ContentDataModel
from main.core.driver.abstractdriver import AbstractTreeAction
from main.core.ActonTypeEnum import ActionTypeEnum
from PyQt6.QtGui import QStandardItemModel, QStandardItem

@s
class MongoDataResponse(AbstractDataResponse):
    _docs: list = ib()
    _query: str = ib()
    _metaData: dict = ib()

    def toJson(self):
        text = dumps(self._docs, default=str, indent=4)
        return ContentData(text, self._query, self._metaData)

    def toTree(self) -> ContentDataModel:
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Documents"])
        rootItem = model.invisibleRootItem()
        assert rootItem

        for doc in self._docs:
            item = QStandardItem("- {...}")
            item.appendRows(createItems(doc))
            rootItem.appendRow(item)

#        model.setItem(0, 0, rootItem)
        return ContentDataModel(model, self._query, self._metaData)
    
    def metadata(self):
        return self._metaData


class TreeActions(AbstractTreeAction):

    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._itemActions[getattr(method, 'node_type_in')] = {getattr(method, 'action_type') : method}
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'node_type_out')]
        for method in methods:
            self._navActions[getattr(method, 'node_type_in')] = {'default' : method}
        

    @TreePath(node_type_in='connections', node_type_out='databases')
    def retrieveDatabases(self, ctx: dict):
        id = make_session_id()
        references[id] = {'client' : MongoClient(ctx['connectionURI'])}
        databases = references[id]['client'].list_database_names()
        return (databases,id)


    @TreePath(node_type_in='databases', node_type_out='collections_holder')
    def retrieveCollectionsHolding(self, ctx: dict):
        return ([ 'collections', 'indexes' ],ctx['sessionID'])


    @TreePath(node_type_in='collections_holder', node_type_out='collections')
    def retrieveCollections(self, ctx: dict):
        id = ctx['sessionID']
        client = references[id]['client']
        dbName = ctx['path'][0]
        db = client[ctx['path'][0]]
        references[id][dbName] = db
        collections = db.list_collection_names()
        return (collections,id)
        

    @ItemAction(node_type_in='collections', action_type = ActionTypeEnum.CLICK)
    def retrieveFirstDocuments(self, ctx: dict):
        return getDocuments(ctx)


def getDocuments(ctx: dict, curPage: int = 0, dimPage: int = 25):
    id = ctx['sessionID']
    dbName = ctx['path'][0]
    colName = ctx['path'][2]
    query = f"db.{colName}.find()"

    db = references[id][dbName]
    col: Collection = db[colName]

    numDocs = col.estimated_document_count()
    skip = curPage * dimPage
    lastPage = numDocs / dimPage - 1

    docs = list()
    for doc in col.find().skip(skip).limit(dimPage):
        docs.append(doc)
    
    metaData = ctx.copy()
    metaData['cur_page'] = curPage
    metaData['last_page'] = lastPage
    return MongoDataResponse(docs, query, metaData)


def createItems(doc: dict) -> list:
    qsi_list = list()
    for key, value in doc.items():
        if isinstance(value, dict):
            qsi = QStandardItem(f"{key}: {{...}}")
            qsi.appendRows(createItems(value))
        elif isinstance(value, list):
            qsi = QStandardItem(f"{key}: [...]")
            for item in value:
                if isinstance(item, dict):
                    qsi_arr = QStandardItem("- {...}")
                    qsi_arr.appendRows(createItems(item))
                    qsi.appendRow(qsi_arr)
                else:
                    qsi.appendRow(QStandardItem(f"- {item}"))
        else:
            qsi = QStandardItem(f"{key}: {str(value)}")

        qsi_list.append(qsi)

    return qsi_list

    