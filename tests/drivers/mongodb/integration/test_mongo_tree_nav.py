from itertools import islice
import pytest
import pytest_docker
from pymongo import MongoClient
from drivers.mongodb.treeactionrules import MongoDataResponse, TreeActions

@pytest.fixture(scope="module")
def docker_compose_file(pytestconfig):
    return str(pytestconfig.rootpath / "playground/mongodb/compose.yml")

@pytest.fixture(scope="module")
def mongo_service(docker_services):
    host = "localhost"
    port = 27017

    def is_mongo_responsive():
        conn = None
        try:
            if conn is None:
                conn = MongoClient(host, port)

            conn.close()
            return True
        except Exception:
            return False
        
    docker_services.wait_until_responsive(timeout=60.0, pause=2, check=lambda: is_mongo_responsive() != False)
    yield True


def test_mongo_tree_navigation(mongo_service):
    ctx = {"connection_uri": "mongodb://localhost:27017"}

    tree_action = TreeActions()
    method = tree_action.retrieveDatabases.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ['admin', 'config', 'local', 'testdb']

    ctx['sessionID'] = result[1]
    ctx['path'] = [result[0][3]]
    
    method = tree_action.retrieveDatabaseObjHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == [ 'collections' ]
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveCollections.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == [ 'firstcollection', 'secondcollection', 'thirdcollection' ]

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveFirstDocuments.__wrapped__
    data: MongoDataResponse  = method(tree_action, ctx)

    assert [ (doc.pop('name'),doc.pop('age')) for doc in data._docs[:3] ] == [ ("Alice", 25 ), ("Bob", 30), ("Charlie", 35) ]


    method = tree_action.retrieveCollectionsObjHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ['indexes']
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveIndexes.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ["('_id_', {'v': 2, 'key': [('_id', 1)]})"]
    assert result[1] == ctx['sessionID']
    