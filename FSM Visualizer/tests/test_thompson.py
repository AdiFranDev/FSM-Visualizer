"""Tests for Thompson's construction algorithm."""

import pytest
from src.algorithms.thompson import thompson_construction


def test_simple_character():
    """Test single character regex."""
    enfa = thompson_construction("a")
    
    assert enfa.accepts("a")
    assert not enfa.accepts("")
    assert not enfa.accepts("b")
    assert not enfa.accepts("aa")


def test_concatenation():
    """Test concatenation."""
    enfa = thompson_construction("abc")
    
    assert enfa.accepts("abc")
    assert not enfa.accepts("")
    assert not enfa.accepts("ab")
    assert not enfa.accepts("abcd")


def test_alternation():
    """Test alternation (OR)."""
    enfa = thompson_construction("a|b")
    
    assert enfa.accepts("a")
    assert enfa.accepts("b")
    assert not enfa.accepts("")
    assert not enfa.accepts("ab")
    assert not enfa.accepts("c")


def test_kleene_star():
    """Test Kleene star."""
    enfa = thompson_construction("a*")
    
    assert enfa.accepts("")
    assert enfa.accepts("a")
    assert enfa.accepts("aa")
    assert enfa.accepts("aaa")
    assert not enfa.accepts("b")


def test_plus():
    """Test plus operator."""
    enfa = thompson_construction("a+")
    
    assert not enfa.accepts("")
    assert enfa.accepts("a")
    assert enfa.accepts("aa")
    assert enfa.accepts("aaa")


def test_complex_regex():
    """Test complex regular expression."""
    enfa = thompson_construction("(a|b)*abb")
    
    assert enfa.accepts("abb")
    assert enfa.accepts("aabb")
    assert enfa.accepts("babb")
    assert enfa.accepts("abababb")
    assert not enfa.accepts("")
    assert not enfa.accepts("ab")
    assert not enfa.accepts("abba")


def test_binary_strings():
    """Test binary string regex."""
    enfa = thompson_construction("(0|1)*00(0|1)*")
    
    assert enfa.accepts("00")
    assert enfa.accepts("000")
    assert enfa.accepts("100")
    assert enfa.accepts("001")
    assert enfa.accepts("10011")
    assert not enfa.accepts("")
    assert not enfa.accepts("0")
    assert not enfa.accepts("1")
    assert not enfa.accepts("010101")
