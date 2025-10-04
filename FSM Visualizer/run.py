"""Launcher script for FSM Visualizer."""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Run the application."""
    try:
        # Import Qt compatibility layer
        from src.qt_compat import QApplication, QT_LIBRARY
        print(f"Using {QT_LIBRARY} for GUI")
    except ImportError as e:
        print("="*70)
        print("ERROR: Qt library not found")
        print("="*70)
        print(f"\nDetails: {e}")
        print("\nPlease install PyQt6 or PySide6:")
        print("  pip install PyQt6")
        print("or")
        print("  pip install PySide6")
        print("="*70)
        sys.exit(1)
    
    # Import main window
    from src.gui.main_window import MainWindow
    
    # Create and run application
    app = QApplication(sys.argv)
    app.setApplicationName("FSM Visualizer")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
