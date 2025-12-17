from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QComboBox, QDialogButtonBox,
    QVBoxLayout, QFormLayout, QWidget, QGroupBox, QLabel, QListView
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
        if connection_name:
            self._initial_connection = ConfigManager.retrieveConnection(connection_name)
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

        general_layout.addRow("Connction name:", self.name_input)
        general_layout.addRow("Database type:", self.type_combo)
        main_layout.addWidget(general_group)

        self.uri_group = QGroupBox("Connection uri details")
        uri_layout = QFormLayout(self.uri_group)
        
        self.connection_uri_input = QLineEdit()
        self.connection_uri_input.setPlaceholderText("es: postgresql://<user>:<pass>@<host>:<port>/<dbname>")
        uri_layout.addRow("Connection uri", self.connection_uri_input)
        
        self.host_port_group = QGroupBox("Credential details")
        host_port_layout = QFormLayout(self.host_port_group)
        
        self.host_input = QLineEdit()
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("e.g., 5432")
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        host_port_layout.addRow("Host:", self.host_input)
        host_port_layout.addRow("Port:", self.port_input)
        host_port_layout.addRow("User:", self.user_input)
        host_port_layout.addRow("Password:", self.password_input)
        
        main_layout.addWidget(self.uri_group)
        main_layout.addWidget(self.host_port_group)
        
        self.status_input = QLineEdit()
        self.status_input.setReadOnly(True)
        self.status_input.setVisible(False)
        self.status_input.setStyleSheet("color: red;")
        main_layout.addWidget(self.status_input)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        main_layout.addWidget(self.button_box)
        
    def _populateUI(self):
        if self._initial_connection:
            conn = self._initial_connection
            self.setWindowTitle(f"Update connection: {conn.name}")
            
            self.name_input.setText(conn.name or "")
            index = self.type_combo.findText(conn.type.label)
            if index != -1:
                self.type_combo.setCurrentIndex(index)
                self.on_index_changed(index)
                
            if conn.connection_uri:
                connection_uri = crypto_manager.decrypt(conn.connection_uri)
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
        inputs = [ self.name_input, self.connection_uri_input, self.host_input, self.port_input ]

        for widget in inputs: widget.textChanged.connect(self._clear_status)

        self.type_combo.currentIndexChanged.connect(self._clear_status)    

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
# 1. Recupero dati grezzi per validazione
        name = self.name_input.text().strip()
        db_type_index = self.type_combo.currentIndex()
        is_uri_mode = self.type_combo.itemData(db_type_index) # flag connectionURIEnabled

        # 2. Validazione Logica
        if not name:
            return self._show_error("Please specify a connection name.")

        if is_uri_mode:
            uri = self.connection_uri_input.text().strip()
            if not uri:
                return self._show_error("The connection URI is mandatory for this type of database.")
        else:
            host = self.host_input.text().strip()
            port_text = self.port_input.text().strip()
            user = self.user_input.text().strip()

            if not host:
                return self._show_error("Please, specify a host name")
            
            if not port_text:
                return self._show_error("Please, specify a port")
            
            if not port_text.isdigit() or not (1 <= int(port_text) <= 65535):
                return self._show_error("The port should be a valid number (1-65535).")
            
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
            self.status_input.setText(f"Errore: {e}")
            raise e
            


    def on_index_changed(self, index):
        flag = self.type_combo.itemData(index)
        self.uri_group.setEnabled(flag)
        self.host_port_group.setEnabled(not flag)


    def _show_error(self, message: str):
        self.status_input.setText(f"⚠️ {message}")
        self.status_input.setVisible(True)
        self.status_input.setFocus()


    def _clear_status(self):
        self.status_input.clear()
        self.status_input.setVisible(False)
