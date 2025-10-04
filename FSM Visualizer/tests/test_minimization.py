"""Tests for DFA minimization algorithm."""

import pytest
from src.models.dfa import DFA
from src.algorithms.minimization import minimize_dfa


def test_minimize_simple_dfa():
    """Test minimization of a simple DFA."""
    dfa = DFA()
    
    # Create DFA with redundant states
    dfa.add_state("q0", is_start=True)
    dfa.add_state("q1")
    dfa.add_state("q2")
    dfa.add_state("q3", is_accept=True)
    dfa.add_state("q4", is_accept=True)
    
    dfa.add_transition("q0", "q1", "0")
    dfa.add_transition("q0", "q2", "1")
    dfa.add_transition("q1", "q3", "0")
    dfa.add_transition("q1", "q2", "1")
    dfa.add_transition("q2", "q1", "0")
    dfa.add_transition("q2", "q4", "1")
    dfa.add_transition("q3", "q3", "0")
    dfa.add_transition("q3", "q3", "1")
    dfa.add_transition("q4", "q4", "0")
    dfa.add_transition("q4", "q4", "1")
    
    minimized = minimize_dfa(dfa)
    
    # Test that language is preserved
    test_strings = ["00", "01", "10", "11", "000", "101"]
    for string in test_strings:
        assert dfa.accepts(string) == minimized.accepts(string)
    
    # Minimized should have fewer states
    assert minimized.get_state_count() <= dfa.get_state_count()


def test_minimize_already_minimal():
    """Test that minimal DFA stays the same."""
    dfa = DFA()
    
    dfa.add_state("q0", is_start=True)
    dfa.add_state("q1", is_accept=True)
    
    dfa.add_transition("q0", "q1", "a")
    dfa.add_transition("q1", "q0", "a")
    
    minimized = minimize_dfa(dfa)
    
    # Should have same number of states
    assert minimized.get_state_count() == 2
    assert minimized.accepts("a")
    assert not minimized.accepts("")


def test_minimize_preserves_language():
    """Test that minimization preserves the language."""
    dfa = DFA()
    
    # Create DFA for (a|b)*abb
    dfa.add_state("q0", is_start=True)
    dfa.add_state("q1")
    dfa.add_state("q2")
    dfa.add_state("q3", is_accept=True)
    
    dfa.add_transition("q0", "q1", "a")
    dfa.add_transition("q0", "q0", "b")
    dfa.add_transition("q1", "q1", "a")
    dfa.add_transition("q1", "q2", "b")
    dfa.add_transition("q2", "q1", "a")
    dfa.add_transition("q2", "q3", "b")
    dfa.add_transition("q3", "q1", "a")
    dfa.add_transition("q3", "q0", "b")
    
    minimized = minimize_dfa(dfa)
    
    test_strings = ["abb", "aabb", "babb", "ab", "bb", ""]
    for string in test_strings:
        assert dfa.accepts(string) == minimized.accepts(string)
