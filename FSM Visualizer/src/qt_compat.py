"""Qt compatibility layer to support both PyQt6 and PySide6."""

import sys

QT_LIBRARY = None

# Try PyQt6 first
try:
    from PyQt6 import QtWidgets, QtCore, QtGui
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import pyqtSignal as Signal
    QT_LIBRARY = "PyQt6"
except ImportError:
    # Fall back to PySide6
    try:
        from PySide6 import QtWidgets, QtCore, QtGui
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Signal
        QT_LIBRARY = "PySide6"
    except ImportError:
        print("ERROR: Neither PyQt6 nor PySide6 is installed!")
        print("\nPlease install one of them:")
        print("  pip install PyQt6")
        print("  or")
        print("  pip install PySide6")
        sys.exit(1)

__all__ = ['QtWidgets', 'QtCore', 'QtGui', 'QApplication', 'Signal', 'QT_LIBRARY']