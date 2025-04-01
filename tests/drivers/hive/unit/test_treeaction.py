from platform import node
import subprocess
import time
import pytest
import psycopg2
from drivers.hive.hive.treeactionrules import PSTreeActions
from core.treepath import ItemAction, TreePath,make_session_id, references, Node
from unittest.mock import MagicMock, patch

@patch("drivers.hive.hive.treeactionrules.hive.Connection")  # Mock della connessione a Hive
@patch("drivers.hive.hive.treeactionrules.make_session_id")  # Mock del generatore di session ID
def test_retrieve_catalogs(mock_make_session_id, mock_hive_Connection):

    mock_make_session_id.return_value = "12345"
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    ctx = dict()
    ctx['host'] = ""
    ctx['port'] = 0

    mock_hive_Connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor  
    
    mock_cursor.fetchall.return_value = [("cat_1",), ("cat_2",), ("cat_3",)]

    tree_action = PSTreeActions()
    method = tree_action.retrieveCatalogs.__wrapped__
    result = method(tree_action, ctx)

    mock_cursor.execute.side_effect = Exception("Errore nella query")
    assert result == (["cat_1","cat_2","cat_3"], "12345")

#@patch("drivers.hive.hive.treeactionrules.hive.connect")  # Mock della connessione a Hive
#@patch("drivers.hive.hive.treeactionrules.make_session_id")  # Mock del generatore di session ID
def test_retrieve_databases():
#conn = references[id]['client']
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    id = "12345"
    ctx = dict()
    ctx['sessionID'] = id
    ctx['path'] = ['cat']
    references[id] = {'client': mock_conn}

#    mock_hive_Connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor  
    
    mock_cursor.fetchall.return_value = [("db1",), ("db2",), ("db3",)]

    tree_action = PSTreeActions()
    method = tree_action.retrieveDatabases.__wrapped__
    result = method(tree_action, ctx)

    mock_cursor.execute.side_effect = Exception("Errore nella query")
    assert result == (["db1","db2","db3"], "12345")


def test_retrieve_obj_holdings():
    ctx = dict()
    ctx['sessionID'] = "12345"

    tree_action = PSTreeActions()
    method = tree_action.retrieveObjHolding.__wrapped__
    result = method(tree_action, ctx)

    assert result == (['tables', 'views', 'indexes', 'procedures'], "12345")


def test_retrieve_tables():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    id = "12345"
    ctx = dict()
    ctx['sessionID'] = id
    ctx['path'] = ["db_1", "tables"]
    references[id] = {'client': mock_conn}

    mock_conn.cursor.return_value = mock_cursor  
    
    mock_cursor.fetchall.return_value = [("", "tbl_1"), ("", "tbl_2"), ("", "tbl_3")]

    tree_action = PSTreeActions()
    method = tree_action.retrieveTables.__wrapped__
    result = method(tree_action, ctx)

    mock_cursor.execute.side_effect = Exception("Errore nella query")
    assert list(result[0]) == ["tbl_1","tbl_2","tbl_3"]
    assert result[1] == "12345"
