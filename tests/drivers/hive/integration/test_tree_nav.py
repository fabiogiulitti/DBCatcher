import datetime
import pytest
import pytest_docker
from impala.hiveserver2 import HiveServer2Connection
from impala.dbapi import connect
from drivers.hive.hive.treeactionrules import DataResponse, PSTreeActions

@pytest.fixture(scope="module")
def docker_compose_file(pytestconfig):
    return str(pytestconfig.rootpath / "playground/hive/compose.yml")

@pytest.fixture(scope="module")
def web_service(docker_services):
    host = "localhost"
    port = 10009

    def is_hive_responsive():
        try:
            conn: HiveServer2Connection = connect(host=host, port=port, auth_mechanism='PLAIN')
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchall()
            cur.close()
            conn.close()
            return True
        except Exception:
            return False
        
    docker_services.wait_until_responsive(timeout=30.0, pause=3, check=is_hive_responsive)
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
    
    assert [ row[:3] for row in data._rows[:3] ] == [(1, 'AAAAAAAABAAAAAAA', datetime.date(1998,1,1)), (2, 'AAAAAAAACAAAAAAA', datetime.date(1998,1,1)), (3, 'AAAAAAAACAAAAAAA', datetime.date(2001,1,1))]

    method = tree_action.retrieveTabHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result[0] == ['columns']
    assert result[1] == ctx['sessionID']

    ctx['path'].append(result[0][0])

    method = tree_action.retrieveColumns.__wrapped__
    result = method(tree_action, ctx)

    assert result[0][:3] == ['cc_call_center_sk bigint None', 'cc_call_center_id string None', 'cc_rec_start_date date None']
    assert result[1] == ctx['sessionID']
    