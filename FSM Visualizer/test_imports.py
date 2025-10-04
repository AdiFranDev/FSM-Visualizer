"""Test script to verify all imports work correctly."""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("Testing imports...")
print("="*50)

try:
    print("1. Testing Qt compatibility...")
    from src.qt_compat import QtWidgets, QtCore, QtGui, QT_LIBRARY
    print(f"   ✓ Using: {QT_LIBRARY}")
    
    print("2. Testing models...")
    from src.models.dfa import DFA
    from src.models.nfa import NFA, EpsilonNFA
    from src.models.mealy_moore import MealyMachine, MooreMachine
    print("   ✓ Models imported")
    
    print("3. Testing parsers...")
    from src.parsers.json_parser import parse_json_automaton
    from src.parsers.text_parser import parse_text_automaton
    print("   ✓ Parsers imported")
    
    print("4. Testing algorithms...")
    from src.algorithms.thompson import thompson_construction
    from src.algorithms.subset_construction import epsilon_nfa_to_nfa, nfa_to_dfa
    from src.algorithms.minimization import minimize_dfa
    from src.algorithms.conversions import mealy_to_moore, moore_to_mealy
    print("   ✓ Algorithms imported")
    
    print("5. Testing visualization...")
    from src.visualization.graph_renderer import render_automaton
    from src.visualization.simulator import simulate_automaton
    print("   ✓ Visualization imported")
    
    print("6. Testing GUI components...")
    from src.gui.main_window import MainWindow
    print("   ✓ GUI imported")
    
    print("\n" + "="*50)
    print("SUCCESS! All imports working correctly.")
    print("="*50)
    print(f"\nQt Library: {QT_LIBRARY}")
    print("\nTo run the application:")
    print("  python run.py")
    
except ImportError as e:
    print(f"\n✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*50)
    print("Please check your installation:")
    print("  pip install -r requirements.txt")
    print("="*50)
    sys.exit(1)
