from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QComboBox, QDialogButtonBox,
    QVBoxLayout, QFormLayout, QWidget, QGroupBox, QLabel
)
from PyQt6.QtCore import pyqtSignal

from main.core.ActonTypeEnum import DriverTypeEnum
from main.core.config import ConfigManager, crypto_manager
from main.core.config.model.connection import Connection
from main.widgets.utils import DBCSignals


class ConnectionDialog(QDialog):
    """
    Dialog window for managing connections
    """
    connection_saved = pyqtSignal(Connection)

    def __init__(self, parent: Optional[QWidget], dbc_signals: DBCSignals, connection_name: Optional[str] = None):
        super().__init__(parent)
        self.dbc_signals = dbc_signals
        self.setWindowTitle("Database connection management")
        self.setMinimumWidth(600)
        print(f"con name {connection_name}")
        if connection_name:
            print("passo 1")
            self._initial_connection = ConfigManager.retrieveConnection(connection_name)
            print("passo 2")
        else:
            self._initial_connection = None
        self._setupUI()
        self._populateUI()
        self._connectSignals()

        self.show()

    def _setupUI(self):
        main_layout = QVBoxLayout(self)
        
        general_group = QGroupBox("General")
        general_layout = QFormLayout(general_group)

        self.name_input = QLineEdit()
        self.type_combo = QComboBox()
        
        for driver in DriverTypeEnum: self.type_combo.addItem(driver.label, driver.connectionURIEnabled)

        general_layout.addRow("Nome Connessione:", self.name_input)
        general_layout.addRow("Tipo Database:", self.type_combo)
        main_layout.addWidget(general_group)

        self.uri_group = QGroupBox("Connection method")
        uri_layout = QFormLayout(self.uri_group)
        
        self.connection_uri_input = QLineEdit()
        self.connection_uri_input.setPlaceholderText("es: postgresql://user:pass@host:port/dbname")
        uri_layout.addRow("Connection uri", self.connection_uri_input)
        
        self.host_port_group = QGroupBox("Credential details")
        host_port_layout = QFormLayout(self.host_port_group)
        
        self.host_input = QLineEdit()
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("e.g., 5432")
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        #self.password_input.setEchoMode(QLineEdit.Password)

        host_port_layout.addRow("Host:", self.host_input)
        host_port_layout.addRow("Porta:", self.port_input)
        host_port_layout.addRow("Utente:", self.user_input)
        host_port_layout.addRow("Password:", self.password_input)
        
        main_layout.addWidget(self.uri_group)
        main_layout.addWidget(self.host_port_group)
        
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.status_label)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        main_layout.addWidget(self.button_box)
        
    def _populateUI(self):
        if self._initial_connection:
            conn = self._initial_connection
            print(conn)
            self.setWindowTitle(f"Update connection: {conn.name}")
            
            self.name_input.setText(conn.name or "")
            index = self.type_combo.findText(conn.type.label)
            if index != -1:
                self.type_combo.setCurrentIndex(index)
                self.on_index_changed(index)
                
            if conn.connection_uri:
                connection_uri = crypto_manager.decrypt(conn.connection_uri)
                print(connection_uri)
                self.connection_uri_input.setText(connection_uri)
            self.host_input.setText(conn.host or "")
            self.port_input.setText(str(conn.port) if conn.port else "")
            self.user_input.setText(conn.user or "")
            if conn.password:
                password = crypto_manager.decrypt(conn.password)
                self.password_input.setText(password)
        else:
            self.on_index_changed(1)

            
    def _connectSignals(self):
        self.button_box.accepted.connect(self._validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        self.type_combo.currentIndexChanged.connect(self.on_index_changed)
        

    def _getInputValues(self) -> Dict[str, Any]:
        port_text = self.port_input.text().strip()
        port = int(port_text) if port_text.isdigit() else None
        
        connection_uri = self.connection_uri_input.text().strip()
        if connection_uri and '' != connection_uri:
            connection_uri = crypto_manager.encrypt(connection_uri)
        password = self.password_input.text().strip()
        if password and '' != password:
            password = crypto_manager.encrypt(password)

        result = {
            'name': self.name_input.text().strip() or None,
            'type': self.type_combo.currentText(),
            'connection_uri': connection_uri or None,
            'host': self.host_input.text().strip() or None,
            'port': port,
            'user': self.user_input.text().strip() or None,
            'password': password or None,
        }

        return {k: v for k, v in result.items() if v is not None}


    def _validate_and_accept(self):
        values = self._getInputValues()
        
        try:
            Connection(values)
            if not self._initial_connection:
                ConfigManager.addConnection(values)
            else:
                ConfigManager.updateConnection(values)
            self.dbc_signals.connection_added.emit(values)
            self.accept()
            
        except Exception as e:
            self.status_label.setText(f"Errore: {e}")
            raise e
            


    def on_index_changed(self, index):
        flag = self.type_combo.itemData(index)
        self.uri_group.setEnabled(flag)
        self.host_port_group.setEnabled(not flag)

