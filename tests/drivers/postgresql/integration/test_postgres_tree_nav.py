import datetime
from itertools import islice
from textwrap import wrap
from types import MethodType, MethodWrapperType
from typing import Any, cast
import pytest
import pytest_docker
import psycopg2

from drivers.postgresql.postgresql.treeactionrules import DataResponse, PSTreeActions
from main.core.driver.abstractdataresponse import TextResponse


@pytest.fixture(scope="module")
def docker_compose_file(pytestconfig):
    return str(pytestconfig.rootpath / "playground/postgresql/compose.yml")

@pytest.fixture(scope="module")
def web_service(docker_services):
    host = "localhost"
    port = 5432
    user = "testuser"
    password = "testpassword"
    db_name = "testdb"

    def is_postgres_responsive():
        conn = None
        try:
            if conn is None:
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    dbname=db_name
                )

            conn.close()
            return True
        except Exception:
            return False
        
    docker_services.wait_until_responsive(timeout=30.0, pause=1, check=lambda: is_postgres_responsive() != False)
    yield True


def test_web_service(web_service):
    ctx = dict()
    ctx['connection_uri'] = "postgresql://testuser:testpassword@localhost:5432/testdb"

    tree_action = PSTreeActions()
    method = tree_action.retrieveDatabases.__wrapped__ # type: ignore
    result = method(tree_action, ctx)

    assert result[0][:3] == ['postgres', 'testdb']

    ctx['sessionID'] = result[1]
    ctx['path'] = [result[0][1]]
    
    method = tree_action.retrieveSchemas.__wrapped__ # type: ignore
    result = method(tree_action, ctx)

    schemas = list(result[0])[:3]
    assert schemas == ['public', 'comics', 'information_schema']

    ctx['sessionID'] = result[1]
    ctx['path'].append(schemas[1])

    method = tree_action.retrieveSchemaHolding.__wrapped__ # type: ignore
    result = method(tree_action, ctx)

    schema_objects = list(result[0])
    assert schema_objects == ['tables', 'views', 'materialized views', 'functions', 'sequences']
    assert result[1] == ctx['sessionID']


    ## Testing tables branch expansion
    ctx['path'].append(schema_objects[0])

    method = tree_action.retrieveTables.__wrapped__ # type: ignore
    result = method(tree_action, ctx)

    tables = list(result[0])
    assert tables == ['characters', 'users']
    assert result[1] == ctx['sessionID']

    ctx['path'].append(tables[0])

    method = tree_action.retrieveFirstRowsTable.__wrapped__ # type: ignore
    response: DataResponse = method(tree_action, ctx)
    rows = response.rows[:2]
    assert rows == [(7, 'Brett Diaz', 'DC', datetime.date(1953, 10, 17), 'Debra Jones', 'Female', 'Alien', 'Good'), (11, 'Daniel Murphy', 'DC', datetime.date(1951, 12, 22), 'Andrew Johnson', 'Female', 'Robot','Good')]
    
    method = tree_action.retrieveTabHolding.__wrapped__ # type: ignore
    table_objects = method(tree_action, ctx)
    assert table_objects[0] == ['columns', 'indexes', 'partitions']

    ctx['path'].append(table_objects[0][0])
    method = tree_action.retrieveColumns.__wrapped__ # type: ignore
    result = method(tree_action, ctx)
    columns = list(result[0])
    assert columns[:2] == ['id integer None', 'name character varying 100']

    # Testing list of table indexes. Overwrite the last item of the tree path to substitute columns, used in the previous call
    ctx['path'][-1] = table_objects[0][1]
    method = tree_action.retrieveIndexes.__wrapped__ # type: ignore
    result = method(tree_action, ctx)
    indexes = list(result[0])
    assert indexes == ['characters_pkey']

    # Testing list of partitions. Overwrite the last item of the tree path to substitute indexes, used in the previous call
    ctx['path'][-1] = table_objects[0][2]
    method = tree_action.retrieveFirstPartitions.__wrapped__ # type: ignore
    result = method(tree_action, ctx)
    partitions = list(result[0])
    assert partitions == ['characters_dc','characters_default']

    ctx['path'].append(partitions[0])
    method = tree_action.retrieveFirstRowsPartition.__wrapped__ # type: ignore
    response: DataResponse = method(tree_action, ctx)
    rows = response.rows[:2]
    assert rows[:2] == [(7, 'Brett Diaz', 'DC', datetime.date(1953, 10, 17), 'Debra Jones', 'Female', 'Alien', 'Good'), (11, 'Daniel Murphy', 'DC', datetime.date(1951, 12, 22), 'Andrew Johnson', 'Female', 'Robot', 'Good')]

    # Retrieve table ddl
    del ctx['path'][-2:]
    method = tree_action.retrieveTableDDL.__wrapped__ # type: ignore
    text_response: TextResponse = method(tree_action, ctx)

    assert text_response.toPlainText().results.splitlines()[:2] == ['CREATE TABLE comics."characters" (', '    "id" integer NOT NULL DEFAULT nextval(\'comics.characters_id_seq\'::regclass),']

    del ctx['path'][-2:]
        

    ## Testing views branch expansion
    ctx['path'].append(schema_objects[1])
    method = tree_action.retrieveViews.__wrapped__ # type: ignore
    result = method(tree_action, ctx)
    views = list(result[0])
    assert views == ['character_details']

    ctx['path'].append(views[0])
    method = tree_action.retrieveFirstRowsView.__wrapped__ # type: ignore
    response: DataResponse = method(tree_action, ctx)
    rows = [r[:8] for r in response.rows[:2]]
    assert rows == [(7, 'Brett Diaz', 'DC', datetime.date(1953, 10, 17), 'Debra Jones', 'Female', 'Alien', 'Good'), (11, 'Daniel Murphy', 'DC', datetime.date(1951, 12, 22), 'Andrew Johnson', 'Female', 'Robot','Good')]

    method = tree_action.retrieveViewDDL.__wrapped__ # type: ignore
    text_response: TextResponse = method(tree_action, ctx)

    assert text_response.toPlainText().results.splitlines()[:2] == ['CREATE view comics.character_details AS', ' SELECT id,'] 

    del ctx['path'][-2:]

    ## Testing materialized views branch expansion
    ctx['path'].append(schema_objects[2])
    method = tree_action.retrieveMaterializedViews.__wrapped__ # type: ignore
    result = method(tree_action, ctx)
    mat_views = list(result[0])
    assert mat_views == ['character_details_json']

    ctx['path'].append(mat_views[0])
    method = tree_action.retrieveFirstRowsMatView.__wrapped__ # type: ignore
    response: DataResponse = method(tree_action, ctx)
    rows = response.rows[:2]
    assert rows == [(7, {'f1': 'Brett Diaz', 'f2': 'DC', 'f3': '1953-10-17', 'f4': 'Debra Jones', 'f5': 'Female', 'f6': 'Alien', 'f7': 'Good'}), (11, {'f1': 'Daniel Murphy', 'f2': 'DC', 'f3': '1951-12-22', 'f4': 'Andrew Johnson', 'f5': 'Female', 'f6': 'Robot', 'f7': 'Good'})]

    method = tree_action.retrieveMaterializedViewDDL.__wrapped__ # type: ignore
    text_response: TextResponse = method(tree_action, ctx)

    assert text_response.toPlainText().results.splitlines()[:2] == ['CREATE materilized view comics.character_details_json AS', ' SELECT id,']

    del ctx['path'][-2:]


    ## Testing functions branch expansion
    ctx['path'].append(schema_objects[3])

    method = tree_action.retrieveFunctions.__wrapped__ # type: ignore
    result = method(tree_action, ctx)
    functions = list(islice(result[0], 2))
    assert functions == ['copy_characters (PROCEDURE)', 'days_since_jan1 (FUNCTION)']

    ctx['path'].append(functions[0].split(' ')[0])

    method = tree_action.retrieveFunctionDDL.__wrapped__ # type: ignore
    text_response: TextResponse = method(tree_action, ctx)

    assert text_response.toPlainText().results.splitlines()[:2] == ['CREATE OR REPLACE PROCEDURE comics.copy_characters()', ' LANGUAGE plpgsql']

    del ctx['path'][-2:]

