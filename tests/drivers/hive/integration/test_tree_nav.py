import pytest
import pytest_docker
from pyhive import hive

from drivers.hive.hive.treeactionrules import DataResponse, PSTreeActions

@pytest.fixture(scope="module")
def docker_compose_file(pytestconfig):
    return str(pytestconfig.rootpath / "playground/hive/compose.yml")

@pytest.fixture(scope="module")
def web_service(docker_services):
#    host = "kyuubi.novobancotools-uat.objectway.com"
    host = "localhost"
    port = 10009

    def is_hive_responsive():
        conn = None
        try:
            if conn is None:
                conn = hive.Connection(host=host, port=port)

            conn.close()
            return True
        except Exception:
            return False
        
    docker_services.wait_until_responsive(timeout=30.0, pause=1, check=lambda: is_hive_responsive() != False)
    yield True


def test_web_service(web_service):
    ctx = dict()
    ctx['host'] = "localhost"
    ctx['port'] = 10009
    

    tree_action = PSTreeActions()
    method = tree_action.retrieveCatalogs.__wrapped__
    result = method(tree_action, ctx)

    assert result[0][:3] == ['spark_catalog', 'tpcds', 'tpch']

    ctx['sessionID'] = result[1]
    ctx['path'] = [result[0][1]]
    
    method = tree_action.retrieveDatabases.__wrapped__
    result = method(tree_action, ctx)

    assert result[0][:4] == ['sf0', 'tiny', 'sf1', 'sf10']

    ctx['path'].append(result[0][3])

    method = tree_action.retrieveObjHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ['tables', 'views', 'indexes', 'procedures']
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveTables.__wrapped__
    result = method(tree_action, ctx)

    assert result[0][:3] == ['call_center', 'catalog_page', 'catalog_returns']
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveFirstRows.__wrapped__
    data: DataResponse = method(tree_action, ctx)
    
    assert [ row[:3] for row in data._rows[:3] ] == [(1, 'AAAAAAAABAAAAAAA', '1998-01-01'), (2, 'AAAAAAAACAAAAAAA', '1998-01-01'), (3, 'AAAAAAAACAAAAAAA', '2001-01-01')]

    method = tree_action.retrieveTabHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ['columns']
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveColumns.__wrapped__
    result = method(tree_action, ctx)

    assert result[0][:3] == ['cc_call_center_sk bigint None', 'cc_call_center_id string None', 'cc_rec_start_date date None']
    assert result[1] == ctx['sessionID']
    