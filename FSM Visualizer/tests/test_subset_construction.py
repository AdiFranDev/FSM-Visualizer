"""Tests for subset construction algorithms."""

import pytest
from src.models.nfa import NFA, EpsilonNFA
from src.algorithms.subset_construction import epsilon_nfa_to_nfa, nfa_to_dfa
from src.algorithms.thompson import thompson_construction


def test_epsilon_nfa_to_nfa():
    """Test epsilon-NFA to NFA conversion."""
    # Create epsilon-NFA from regex
    enfa = thompson_construction("a*b")
    
    # Convert to NFA
    nfa = epsilon_nfa_to_nfa(enfa)
    
    # Test acceptance
    assert nfa.accepts("b")
    assert nfa.accepts("ab")
    assert nfa.accepts("aab")
    assert not nfa.accepts("")
    assert not nfa.accepts("a")


def test_nfa_to_dfa_simple():
    """Test simple NFA to DFA conversion."""
    nfa = NFA()
    nfa.add_state("q0", is_start=True)
    nfa.add_state("q1")
    nfa.add_state("q2", is_accept=True)
    
    nfa.add_transition("q0", "q1", "a")
    nfa.add_transition("q0", "q1", "b")
    nfa.add_transition("q1", "q2", "a")
    
    dfa = nfa_to_dfa(nfa)
    
    assert dfa.accepts("aa")
    assert dfa.accepts("ba")
    assert not dfa.accepts("")
    assert not dfa.accepts("a")
    assert not dfa.accepts("b")


def test_nfa_to_dfa_complex():
    """Test complex NFA to DFA conversion."""
    # Create NFA from regex
    enfa = thompson_construction("(a|b)*abb")
    nfa = epsilon_nfa_to_nfa(enfa)
    dfa = nfa_to_dfa(nfa)
    
    assert dfa.accepts("abb")
    assert dfa.accepts("aabb")
    assert dfa.accepts("babb")
    assert not dfa.accepts("")
    assert not dfa.accepts("ab")
    
    # Check that it's deterministic
    is_valid, msg = dfa.validate()
    assert is_valid


def test_subset_construction_preserves_language():
    """Test that conversions preserve the language."""
    test_strings = ["", "a", "aa", "ab", "ba", "abb", "aab", "bba"]
    regex = "a*b+"
    
    enfa = thompson_construction(regex)
    nfa = epsilon_nfa_to_nfa(enfa)
    dfa = nfa_to_dfa(nfa)
    
    for string in test_strings:
        assert enfa.accepts(string) == nfa.accepts(string)
        assert nfa.accepts(string) == dfa.accepts(string)
