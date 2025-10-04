"""Launcher script with dependency checking."""

import sys
import subprocess

def check_pyqt6():
    """Check if PyQt6 is working."""
    try:
        from PyQt6 import QtCore
        print("✓ PyQt6 is installed correctly")
        return True
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        print("\nTo fix, run:")
        print("  pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y")
        print("  pip install PyQt6==6.6.1")
        return False

def check_graphviz():
    """Check if graphviz is installed."""
    try:
        import graphviz
        print("✓ graphviz Python package is installed")
    except ImportError:
        print("✗ graphviz not installed")
        print("  Run: pip install graphviz==0.20.1")
        return False
    
    try:
        subprocess.run(['dot', '-V'], capture_output=True, timeout=5)
        print("✓ Graphviz system binary is installed")
        return True
    except:
        print("✗ Graphviz system binary not found")
        print("  Install from: https://graphviz.org/download/")
        return False

if __name__ == "__main__":
    print("FSM Visualizer - Dependency Check")
    print("=" * 50)
    
    pyqt_ok = check_pyqt6()
    graphviz_ok = check_graphviz()
    
if pyqt_ok and graphviz_ok:
    print("\n✓ All dependencies OK!")
    print("Launching application...\n")
    from src.main import main
    main()
else:
    print("\n✗ Please fix the issues above first")
    sys.exit(1)
