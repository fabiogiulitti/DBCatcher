from PyQt5.QtWidgets import QApplication, QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from pymongo import MongoClient


def create_mongo_model():
    client = MongoClient('mongodb://localhost:27017/')  # Modifica l'URI se necessario

    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(['MongoDB'])
    # Ottieni la lista dei database
    databases = client.list_database_names()

    for db_name in databases:
        db_item = QStandardItem(db_name)
        model.appendRow(db_item)
        
        db = client[db_name]
        collections = db.list_collection_names()
        for coll_name in collections:
            coll_item = QStandardItem(coll_name)
            db_item.appendRow(coll_item)

    return model

