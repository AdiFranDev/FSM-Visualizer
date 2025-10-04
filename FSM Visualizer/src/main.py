"""Main entry point for FSM Visualizer application."""

import sys
import os

# Add parent directory to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def main():
    """Run the application."""
    try:
        from src.qt_compat import QApplication, QT_LIBRARY
        print(f"Using {QT_LIBRARY} for GUI")
    except ImportError as e:
        print("="*70)
        print("ERROR: Qt library failed to import")
        print("="*70)
        print(f"\nDetails: {e}")
        print("\nPlease install PyQt6 or PySide6:")
        print("\n  pip install PyQt6==6.6.1")
        print("\nor")
        print("\n  pip install PySide6")
        print("\nFor PyQt6 DLL issues on Windows, try:")
        print("  pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y")
        print("  pip install PyQt6==6.5.0")
        print("="*70)
        sys.exit(1)
    
    from src.gui.main_window import MainWindow
    
    app = QApplication(sys.argv)
    app.setApplicationName("FSM Visualizer")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    import traceback
    traceback.print_exc()
    sys.exit(1)
