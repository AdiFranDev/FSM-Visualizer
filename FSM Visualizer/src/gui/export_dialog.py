"""Dialog for exporting graph visualizations."""

from ..qt_compat import QtWidgets
from ..qt_compat import QtWidgets as QW

QDialog = QW.QDialog
QVBoxLayout = QW.QVBoxLayout
QHBoxLayout = QW.QHBoxLayout
QLabel = QW.QLabel
QLineEdit = QW.QLineEdit
QPushButton = QW.QPushButton
QComboBox = QW.QComboBox
QFileDialog = QW.QFileDialog


class ExportDialog(QDialog):
    """Dialog for graph export options."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Graph")
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # File path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("File Path:"))
        self.path_field = QLineEdit()
        path_layout.addWidget(self.path_field)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["png", "svg", "pdf", "jpg"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.accept)
        button_layout.addWidget(export_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def browse_path(self):
        """Open file browser."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Graph", "",
            "PNG Files (*.png);;SVG Files (*.svg);;PDF Files (*.pdf);;All Files (*)"
        )
        
        if filename:
            # Remove extension if present
            for ext in ['.png', '.svg', '.pdf', '.jpg']:
                if filename.endswith(ext):
                    filename = filename[:-len(ext)]
                    break
            
            self.path_field.setText(filename)
    
    def get_export_info(self) -> tuple[str, str]:
        """Get export file path and format."""
        return self.path_field.text(), self.format_combo.currentText()
