from PyQt6.QtGui import QStandardItem
from pymongo import MongoClient


def create_mongo_model(connectionUri):
    client = MongoClient(connectionUri)
    databases = client.list_database_names()

    db_items = list()

    for db_name in databases:
        db_item = QStandardItem(db_name)
        db_items.append(db_item)

        colls_item = QStandardItem("collections")
        db_item.appendRow(colls_item)
        db = client[db_name]
        collections = db.list_collection_names()
        for coll_name in collections:
            coll_item = QStandardItem(coll_name)
            colls_item.appendRow(coll_item)

    return db_items

