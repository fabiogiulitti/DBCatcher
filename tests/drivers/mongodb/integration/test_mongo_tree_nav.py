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
    ctx = dict()
    ctx['connectionURI'] = "mongodb://localhost:27017"

    tree_action = TreeActions()
    method = tree_action.retrieveDatabases.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ['admin', 'config', 'local', 'testdb']

    ctx['sessionID'] = result[1]
    ctx['path'] = [result[0][3]]
    
    method = tree_action.retrieveCollectionsHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == [ 'collections', 'indexes' ]
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveCollections.__wrapped__
    result = method(tree_action, ctx)

    sortedResult = sorted(result[0][:3]) 
    assert sortedResult == [ 'firstcollection', 'secondcollection', 'thirdcollection' ]

    ctx['path'].append(sortedResult[0])

    method = tree_action.retrieveFirstDocuments.__wrapped__
    data: MongoDataResponse  = method(tree_action, ctx)

    assert [ (doc.pop('name'),doc.pop('age')) for doc in data._docs[:3] ] == [ ("Alice", 25 ), ("Bob", 30), ("Charlie", 35) ]


    # method = tree_action.retrieveTabHolding.__wrapped__
    # result = method(tree_action, ctx)

    # assert result[0] == ['columns']
    # assert result[1] == ctx['sessionID']

    # ctx['path'].append(result[0][0])

    # method = tree_action.retrieveColumns.__wrapped__
    # result = method(tree_action, ctx)

    # assert result[0][:3] == ['cc_call_center_sk bigint None', 'cc_call_center_id string None', 'cc_rec_start_date date None']
    # assert result[1] == ctx['sessionID']
    