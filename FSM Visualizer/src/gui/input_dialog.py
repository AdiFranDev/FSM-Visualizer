"""Input dialog for simple text input."""

from ..qt_compat import QtWidgets

QDialog = QtWidgets.QDialog
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QLabel = QtWidgets.QLabel
QLineEdit = QtWidgets.QLineEdit
QPushButton = QtWidgets.QPushButton


class InputDialog(QDialog):
    """Simple input dialog."""
    
    def __init__(self, title: str, prompt: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.init_ui(prompt)
    
    def init_ui(self, prompt: str):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Prompt label
        label = QLabel(prompt)
        layout.addWidget(label)
        
        # Input field
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def get_input(self) -> str:
        """Get the input text."""
        return self.input_field.text()
