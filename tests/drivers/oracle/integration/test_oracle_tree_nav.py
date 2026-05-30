import oracledb
import pytest
from pytest_docker.plugin import get_docker_services

from drivers.oracle.treeactionrules import DataResponse, ORTreeActions
from main.core.config import crypto_manager
from main.core.driver.abstractdataresponse import TextResponse


# Garantisce che la chiave Fernet esista nel keyring locale: senza,
# crypto_manager.decrypt() asserisce e fa fallire retrieveSchemas.
crypto_manager.verifyKey()


CONNECTION_URI = "oracle://testuser:testpassword@localhost:1521/FREEPDB1"


@pytest.fixture(scope="module")
def docker_compose_file(pytestconfig):
    return str(pytestconfig.rootpath / "playground/oracle/compose.yml")

@pytest.fixture(scope="module")
def oracle_service(docker_services):
    def is_responsive():
        try:
            conn = oracledb.connect(
                user="testuser",
                password="testpassword",
                dsn="localhost:1521/FREEPDB1",
            )
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM dual")
            cur.fetchone()
            cur.close()
            conn.close()
            return True
        except Exception:
            return False

    docker_services.wait_until_responsive(timeout=30.0, pause=3, check=is_responsive)
    yield True


def test_oracle_tree_navigation(oracle_service):
    ctx = {"connection_uri": CONNECTION_URI}

    tree_action = ORTreeActions()

    # connections → schemas
    method = tree_action.retrieveSchemas.__wrapped__  # type: ignore[attr-defined]
    schemas, s_id = method(tree_action, ctx)
    assert "TESTUSER" in schemas

    # schemas → schema_obj_hold (static list)
    ctx["sessionID"] = s_id
    ctx["path"] = ["TESTUSER"]
    method = tree_action.retrieveSchemaHolding.__wrapped__  # type: ignore[attr-defined]
    holdings, _ = method(tree_action, ctx)
    assert holdings == [
        "tables", "views", "materialized views", "procedures", "sequences",
    ]

    # tables
    ctx["path"].append("tables")
    method = tree_action.retrieveTables.__wrapped__  # type: ignore[attr-defined]
    tables, _ = method(tree_action, ctx)
    assert "CHARACTERS" in tables
    assert "USERS" in tables

    # read first rows
    ctx["path"].append("CHARACTERS")
    method = tree_action.retrieveFirstRowsTable.__wrapped__  # type: ignore[attr-defined]
    response: DataResponse = method(tree_action, ctx)
    cols_lower = [c.lower() for c in response._cols]  # type: ignore[attr-defined]
    assert "name" in cols_lower
    assert "universe" in cols_lower
    assert len(response.rows) >= 4
    universes = {row[cols_lower.index("universe")] for row in response.rows}
    assert {"DC", "Image", "Marvel"}.issubset(universes)

    #subobjects of table
    method = tree_action.retrieveTabHolding.__wrapped__  # type: ignore[attr-defined]
    table_objects, _ = method(tree_action, ctx)
    assert table_objects == ["columns", "indexes"]

    # columns
    ctx["path"].append("columns")
    method = tree_action.retrieveColumns.__wrapped__  # type: ignore[attr-defined]
    columns, _ = method(tree_action, ctx)
    column_names = {c.split(" ", 1)[0] for c in columns}
    assert {"ID", "NAME", "UNIVERSE"}.issubset(column_names)

    # indexes
    ctx["path"][-1] = "indexes"
    method = tree_action.retrieveIndexes.__wrapped__  # type: ignore[attr-defined]
    indexes, _ = method(tree_action, ctx)
    assert "IDX_CHARACTERS_UNIVERSE" in indexes

    # Table DDL
    del ctx["path"][-1]  # remove 'indexes'
    # ctx["path"] now is ["TESTUSER", "tables", "CHARACTERS"]
    method = tree_action.retrieveTableDDL.__wrapped__  # type: ignore[attr-defined]
    text_response: TextResponse = method(tree_action, ctx)
    ddl = text_response.toPlainText().results
    assert "CHARACTERS" in ddl
    assert "CREATE" in ddl.upper()

    # views
    del ctx["path"][-2:]  # remove 'tables', 'CHARACTERS'
    ctx["path"].append("views")
    method = tree_action.retrieveViews.__wrapped__  # type: ignore[attr-defined]
    views, _ = method(tree_action, ctx)
    assert "CHARACTER_DETAILS" in views

    ctx["path"].append("CHARACTER_DETAILS")
    method = tree_action.retrieveFirstRowsView.__wrapped__  # type: ignore[attr-defined]
    response = method(tree_action, ctx)
    assert len(response.rows) >= 4

    method = tree_action.retrieveViewDDL.__wrapped__  # type: ignore[attr-defined]
    text_response = method(tree_action, ctx)
    view_ddl = text_response.toPlainText().results.upper()
    assert "CHARACTERS" in view_ddl
    assert "CHARACTER_DETAILS" in view_ddl

    # materialized views
    del ctx["path"][-2:]
    ctx["path"].append("materialized views")
    method = tree_action.retrieveMaterializedViews.__wrapped__  # type: ignore[attr-defined]
    mviews, _ = method(tree_action, ctx)
    assert "CHARACTER_DETAILS_MV" in mviews

    # MV → first rows
    ctx["path"].append("CHARACTER_DETAILS_MV")
    method = tree_action.retrieveFirstRowsMatView.__wrapped__  # type: ignore[attr-defined]
    response = method(tree_action, ctx)
    assert len(response.rows) >= 4
    mv_universes = {row[[c.lower() for c in response._cols].index("universe")]  # type: ignore[attr-defined]
                    for row in response.rows}
    assert {"DC", "Image", "Marvel"}.issubset(mv_universes)

    # MV DDL
    method = tree_action.retrieveMaterializedViewDDL.__wrapped__  # type: ignore[attr-defined]
    text_response = method(tree_action, ctx)
    mv_ddl = text_response.toPlainText().results.upper()
    assert "CHARACTER_DETAILS_MV" in mv_ddl
    assert "MATERIALIZED VIEW" in mv_ddl

    # sequences
    del ctx["path"][-2:]
    ctx["path"].append("sequences")
    method = tree_action.retrieveSequences.__wrapped__  # type: ignore[attr-defined]
    sequences, _ = method(tree_action, ctx)
    assert "SEQ_DEMO" in sequences

    # procedures
    del ctx["path"][-1]
    ctx["path"].append("procedures")
    method = tree_action.retrieveProcedures.__wrapped__  # type: ignore[attr-defined]
    procs, _ = method(tree_action, ctx)
    proc_label = next((p for p in procs if p.startswith("COPY_CHARACTERS")), None)
    assert proc_label is not None
    assert proc_label.endswith("(PROCEDURE)")

    # Procedure DDL
    ctx["path"].append(proc_label)
    method = tree_action.retrieveProcedureDDL.__wrapped__  # type: ignore[attr-defined]
    text_response = method(tree_action, ctx)
    proc_ddl = text_response.toPlainText().results.upper()
    assert "COPY_CHARACTERS" in proc_ddl
    assert "PROCEDURE" in proc_ddl
