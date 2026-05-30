from unittest.mock import MagicMock, patch

import pytest

from drivers.oracle.treeactionrules import (
    ConnectionStrategy,
    ORTreeActions,
    _q,
    _split_proc_label,
    getRows,
    getTableCount,
)
from main.core.treepath import references


# ── pure-function helpers ────────────────────────────────────────────────────

def test_q_quotes_identifier_and_escapes_internal_quotes():
    assert _q("HR") == '"HR"'
    assert _q('weird"name') == '"weird""name"'


def test_split_proc_label_extracts_name_and_type():
    assert _split_proc_label("DO_STUFF (PROCEDURE)") == ("DO_STUFF", "PROCEDURE")
    assert _split_proc_label("CALC (FUNCTION)") == ("CALC", "FUNCTION")
    assert _split_proc_label("BARE_NAME") == ("BARE_NAME", "PROCEDURE")


# ── ConnectionStrategy.connect ──────────────────────────────────────────────

@patch("drivers.oracle.treeactionrules.oracledb.connect")
def test_connection_strategy_parses_uri(mock_connect):
    ConnectionStrategy.connect({
        "connection_uri": "oracle://testuser:testpassword@localhost:1521/FREEPDB1"
    })
    mock_connect.assert_called_once_with(
        user="testuser",
        password="testpassword",
        dsn="localhost:1521/FREEPDB1",
    )


def test_connection_strategy_rejects_unknown_scheme():
    with pytest.raises(ValueError, match="Unsupported Oracle URI scheme"):
        ConnectionStrategy.connect({"connection_uri": "postgres://x:y@h:1/z"})


def test_connection_strategy_requires_service():
    with pytest.raises(ValueError, match="must include the service name"):
        ConnectionStrategy.connect({"connection_uri": "oracle://u:p@h:1521"})


# ── tree navigation methods (mocked DB) ──────────────────────────────────────

@patch("drivers.oracle.treeactionrules.ConnectionProxy")
@patch("drivers.oracle.treeactionrules.crypto_manager")
@patch("drivers.oracle.treeactionrules.make_session_id")
def test_retrieve_schemas(mock_make_session_id, mock_crypto, mock_proxy_cls):
    mock_make_session_id.return_value = "sess-1"
    mock_crypto.decrypt.side_effect = lambda v: v
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_proxy_cls.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("HR",), ("SCOTT",), ("TESTUSER",)]

    ctx = {"connection_uri": "oracle://u:p@h:1521/SVC"}
    tree_action = ORTreeActions()
    method = tree_action.retrieveSchemas.__wrapped__  # type: ignore[attr-defined]
    result = method(tree_action, ctx)

    assert result == (["HR", "SCOTT", "TESTUSER"], "sess-1")
    assert references["sess-1"]["client"] is mock_conn


def test_retrieve_schema_holding_returns_static_list():
    tree_action = ORTreeActions()
    method = tree_action.retrieveSchemaHolding.__wrapped__  # type: ignore[attr-defined]
    result = method(tree_action, {"sessionID": "sid"})
    assert result == (
        ["tables", "views", "materialized views", "procedures", "sequences"],
        "sid",
    )


def test_retrieve_tables_uses_owner_bind():
    sid = "sid-tables"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("CHARACTERS",), ("USERS",)]
    references[sid] = {"client": mock_conn}

    ctx = {"sessionID": sid, "path": ["TESTUSER", "tables"]}
    tree_action = ORTreeActions()
    method = tree_action.retrieveTables.__wrapped__  # type: ignore[attr-defined]
    result = method(tree_action, ctx)

    assert result == (["CHARACTERS", "USERS"], sid)
    args, kwargs = mock_cursor.execute.call_args
    assert "all_tables" in args[0]
    assert kwargs == {"owner": "TESTUSER"}


def test_retrieve_views_uses_correct_query():
    sid = "sid-views"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("V_DETAILS",)]
    references[sid] = {"client": mock_conn}

    ctx = {"sessionID": sid, "path": ["TESTUSER", "views"]}
    tree_action = ORTreeActions()
    method = tree_action.retrieveViews.__wrapped__  # type: ignore[attr-defined]
    result = method(tree_action, ctx)

    assert result == (["V_DETAILS"], sid)
    assert "all_views" in mock_cursor.execute.call_args[0][0]


def test_retrieve_procedures_includes_object_type_label():
    sid = "sid-proc"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("DO_STUFF", "PROCEDURE"),
        ("CALC", "FUNCTION"),
    ]
    references[sid] = {"client": mock_conn}

    ctx = {"sessionID": sid, "path": ["TESTUSER", "procedures"]}
    tree_action = ORTreeActions()
    method = tree_action.retrieveProcedures.__wrapped__  # type: ignore[attr-defined]
    result = method(tree_action, ctx)

    assert result == (["DO_STUFF (PROCEDURE)", "CALC (FUNCTION)"], sid)


def test_retrieve_columns_formats_column_metadata():
    sid = "sid-cols"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("ID", "NUMBER", 22),
        ("NAME", "VARCHAR2", 100),
    ]
    references[sid] = {"client": mock_conn}

    ctx = {
        "sessionID": sid,
        "path": ["TESTUSER", "tables", "CHARACTERS", "tables_obj_hold"],
    }
    tree_action = ORTreeActions()
    method = tree_action.retrieveColumns.__wrapped__  # type: ignore[attr-defined]
    result = method(tree_action, ctx)

    assert result == (["ID NUMBER 22", "NAME VARCHAR2 100"], sid)
    kwargs = mock_cursor.execute.call_args.kwargs
    assert kwargs == {"owner": "TESTUSER", "tname": "CHARACTERS"}


def test_retrieve_table_ddl_unwraps_clob():
    sid = "sid-ddl"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    clob = MagicMock()
    clob.read.return_value = "  CREATE TABLE FOO ( ID NUMBER )  "
    mock_cursor.fetchone.return_value = (clob,)
    references[sid] = {"client": mock_conn}

    ctx = {
        "sessionID": sid,
        "path": ["TESTUSER", "tables", "FOO"],
    }
    tree_action = ORTreeActions()
    method = tree_action.retrieveTableDDL.__wrapped__  # type: ignore[attr-defined]
    response = method(tree_action, ctx)

    assert response.toPlainText().results == "CREATE TABLE FOO ( ID NUMBER )"
    kwargs = mock_cursor.execute.call_args.kwargs
    assert kwargs == {"otype": "TABLE", "oname": "FOO", "owner": "TESTUSER"}


# ── pagination helpers ──────────────────────────────────────────────────────

def test_get_table_count_computes_last_page():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (450,)

    total, last_page = getTableCount(200, "TESTUSER", "CHARACTERS", mock_conn)

    assert total == 450
    assert last_page == 2  # ceil(450/200 - 1) = ceil(1.25) = 2
    assert '"TESTUSER"."CHARACTERS"' in mock_cursor.execute.call_args[0][0]


def test_get_rows_uses_offset_fetch_pagination():
    sid = "sid-rows"
    mock_conn = MagicMock()
    mock_count_cursor = MagicMock()
    mock_count_cursor.fetchone.return_value = (10,)
    mock_data_cursor = MagicMock()
    mock_data_cursor.description = [("ID",), ("NAME",)]
    mock_data_cursor.fetchall.return_value = [(1, "A"), (2, "B")]
    mock_conn.cursor.side_effect = [mock_count_cursor, mock_data_cursor]
    references[sid] = {"client": mock_conn}

    ctx = {
        "sessionID": sid,
        "path": ["conn", "TESTUSER", "tables", "CHARACTERS"],
    }
    response = getRows(ctx, cur_page=1, dim_page=5)

    query = mock_data_cursor.execute.call_args[0][0]
    assert "OFFSET 5 ROWS" in query
    assert "FETCH NEXT 5 ROWS ONLY" in query
    assert response.rows == [(1, "A"), (2, "B")]
    metadata = response.metadata()
    assert metadata["cur_page"] == 1
    assert metadata["dim_page"] == 5
    assert metadata["tot_result"] == 10
