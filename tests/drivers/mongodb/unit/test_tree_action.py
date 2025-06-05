from pydoc import describe, text
import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtCore import Qt
from drivers.mongodb.treeactionrules import MongoDataResponse, createItems


def test_mongo_data_response():
    dict1 = {
    "user": {
        "id": 101,
        "name": "Alice",
        "email": "alice@example.com"
    },
    "projects": [
        {"name": "Alpha", "status": "completed"},
        {"name": "Beta", "status": "in progress"},
        {"name": "Gamma", "status": "planned"}
    ],
    "skills": ["Python", "JavaScript", "SQL"]
}

    response = MongoDataResponse([dict1],'',{})

    content = response.toTree()
    model = content.results

    assert model.rowCount() == 1
    role = Qt.ItemDataRole.DisplayRole
    doc_index = model.index(0, 0)
    assert model.data(doc_index, role) == '- {...}'
    field0_index = model.index(0, 0, doc_index)
    assert model.data(field0_index, role) == 'user: {...}'
    field00_index = model.index(0, 0, field0_index)
    assert model.data(field00_index, role) == 'id: 101'
    field01_index = model.index(1, 0, field0_index)
    assert model.data(field01_index, role) == 'name: Alice'
    field02_index = model.index(2, 0, field0_index)
    assert model.data(field02_index, role) == 'email: alice@example.com'
    field1_index = model.index(1, 0, doc_index)
    assert model.data(field1_index, role) == 'projects: [...]'
    field11_index = model.index(1, 0, field1_index)
    assert model.data(field11_index, role) == '- {...}'
    field110_index = model.index(0, 0, field11_index)
    assert model.data(field110_index, role) == 'name: Beta'
    field111_index = model.index(1, 0, field11_index)
    assert model.data(field111_index, role) == 'status: in progress'
    field2_index = model.index(2, 0, doc_index)
    assert model.data(field2_index, role) == 'skills: [...]'
    field22_index = model.index(2, 0, field2_index)
    assert model.data(field22_index, role) == '- SQL'
