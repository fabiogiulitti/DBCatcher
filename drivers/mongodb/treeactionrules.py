from core.treepath import TreePath,make_session_id, references
from core.itemaction import ItemAction
from pymongo import MongoClient
from pymongo.collection import Collection
from json import dumps
from widgets.ContentData import ContentData

@TreePath(node_type_in='connections', node_type_out='databases')
def retrieveDatabases(ctx: dict):
    id = make_session_id()
    references[id] = {'client' : MongoClient(ctx['connectionURI'])}
    databases = references[id]['client'].list_database_names()
    return (databases,id)


@TreePath(node_type_in='databases', node_type_out='collections_holder')
def retrieveCollectionsHolding(ctx: dict):
    return (['collections'],ctx['sessionID'])


@TreePath(node_type_in='collections_holder', node_type_out='collections')
def retrieveCollections(ctx: dict):
    id = ctx['sessionID']
    client = references[id]['client']
    dbName = ctx['path'][0]
    db = client[ctx['path'][0]]
    references[id][dbName] = db
    collections = db.list_collection_names()
    return (collections,id)

@ItemAction(node_type_in='collections', action_type='clicked')
def retrieveFirstDocuments(ctx: dict):
    return getDocuments(ctx)

def getDocuments(ctx: dict, curPage: int = 0, dimPage: int = 25):
    id = ctx['sessionID']
    dbName = ctx['path'][0]
    colName = ctx['path'][2]
    db = references[id][dbName]
    col: Collection = db[colName]

    numDocs = col.count()
    skip = curPage * dimPage
    lastPage = numDocs / dimPage - 1

    docs = list()
    for doc in col.find().skip(skip).limit(dimPage):
        docs.append(doc)
    
    text = dumps(docs, default=str, indent=4)
    metaData = ctx.copy()
    metaData['cur_page'] = curPage
    metaData['last_page'] = lastPage
    return ContentData(text, metaData)
