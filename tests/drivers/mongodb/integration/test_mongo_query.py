from itertools import islice
import pytest
import pytest_docker
from pymongo import MongoClient
from drivers.hive.hive.treeactionrules import DataResponse
from drivers.mongodb.queryactionrules import MongoDataResponse, ContentAction, MongoQueryActionDef, references


@pytest.fixture(scope="module")
def docker_compose_file(pytestconfig):
    return str(pytestconfig.rootpath / "playground/mongodb/compose.yml")

@pytest.fixture(scope="module")
def mongo_service(docker_services):
    host = "localhost"
    port = 27017
    conn = None

    def is_mongo_responsive():
        nonlocal conn

        try:
            if conn is None:
                conn = MongoClient(host, port)

            return conn
        except Exception:
            return None
        
    docker_services.wait_until_responsive(timeout=60.0, pause=2, check=lambda: is_mongo_responsive() != False)
    yield conn


def test_mongo_tree_navigation(mongo_service):
    id = '12345'
    ctx = dict()
    ctx['sessionID'] = id
    ctx['path'] = ['testdb', '', 'firstcollection']
    ctx['query'] = 'db.firstcollection.find({},{"name": 1,"age": 1}).sort({"age": -1}).limit(2)'
    db = mongo_service['testdb']
    references[id] = {'testdb' : db}
    
    query_action = MongoQueryActionDef()
    method = query_action._executeQuery.__wrapped__
    data: MongoDataResponse = method(query_action, ctx)

    assert [ (doc.pop('name'),doc.pop('age')) for doc in data._docs[:3] ] == [('Charlie', 35), ('Bob', 30)]

