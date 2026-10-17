from unittest.mock import MagicMock

from drivers.oracle.queryactionrules import executeQuery
from main.core.treepath import references


def _setup_session(sid: str, description, fetch_rows, rowcount=0):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.description = description
    mock_cursor.fetchall.return_value = fetch_rows
    mock_cursor.rowcount = rowcount
    mock_conn.cursor.return_value = mock_cursor
    references[sid] = {"client": mock_conn}
    return mock_cursor


def test_execute_query_appends_fetch_clause_for_select():
    sid = "q1"
    cur = _setup_session(sid, [("ID",)], [(1,), (2,)])
    ctx = {"sessionID": sid, "query": "SELECT id FROM characters"}

    response = executeQuery(ctx, dim_page=50)

    executed = cur.execute.call_args[0][0]
    assert executed.endswith("FETCH FIRST 50 ROWS ONLY")
    assert response.rows == [(1,), (2,)]


def test_execute_query_preserves_existing_fetch_clause():
    sid = "q2"
    cur = _setup_session(sid, [("ID",)], [(1,)])
    ctx = {
        "sessionID": sid,
        "query": "SELECT id FROM characters FETCH FIRST 5 ROWS ONLY",
    }

    executeQuery(ctx, dim_page=200)

    executed = cur.execute.call_args[0][0]
    # Non deve aggiungere un secondo FETCH
    assert executed.upper().count("FETCH FIRST") == 1


def test_execute_query_strips_trailing_semicolon():
    sid = "q3"
    cur = _setup_session(sid, [("ID",)], [(1,)])
    ctx = {"sessionID": sid, "query": "SELECT id FROM characters;"}

    executeQuery(ctx, dim_page=10)

    executed = cur.execute.call_args[0][0]
    assert ";" not in executed


def test_execute_query_returns_affected_rows_for_dml():
    sid = "q4"
    cur = _setup_session(sid, None, [], rowcount=7)
    ctx = {"sessionID": sid, "query": "DELETE FROM characters WHERE id = 99"}

    response = executeQuery(ctx)

    assert response.rows == [[7]]
    # DML non deve essere annotato con FETCH
    executed = cur.execute.call_args[0][0]
    assert "FETCH" not in executed.upper()
