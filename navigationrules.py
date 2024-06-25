from treepath import TreePath,Node, make_session_id, references
from pymongo import MongoClient

#connectionUri = "mongodb://localhost:27017"

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
    print(ctx)
    db = client[ctx['path'][0]]
    collections = db.list_collection_names()
    print(collections)
    return (collections,id)
