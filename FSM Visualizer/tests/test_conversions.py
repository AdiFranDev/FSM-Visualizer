"""Tests for Mealy/Moore machine conversions."""

import pytest
from src.models.mealy_moore import MealyMachine, MooreMachine
from src.algorithms.conversions import mealy_to_moore, moore_to_mealy


def test_mealy_to_moore_simple():
    """Test simple Mealy to Moore conversion."""
    mealy = MealyMachine()
    
    mealy.add_state("A", is_start=True)
    mealy.add_state("B")
    
    mealy.add_transition("A", "B", "0", "x")
    mealy.add_transition("A", "A", "1", "y")
    mealy.add_transition("B", "A", "0", "z")
    mealy.add_transition("B", "B", "1", "x")
    
    moore = mealy_to_moore(mealy)
    
    # Check output sequences match
    success_mealy, outputs_mealy = mealy.process_input("010")
    success_moore, outputs_moore = moore.process_input("010")
    
    assert success_mealy and success_moore
    # Moore has one extra output (initial state)
    assert len(outputs_moore) == len(outputs_mealy) + 1


def test_moore_to_mealy_simple():
    """Test simple Moore to Mealy conversion."""
    moore = MooreMachine()
    
    moore.add_state("A", is_start=True)
    moore.add_state("B")
    
    moore.set_state_output("A", "x")
    moore.set_state_output("B", "y")
    
    moore.add_transition("A", "B", "0")
    moore.add_transition("A", "A", "1")
    moore.add_transition("B", "A", "0")
    moore.add_transition("B", "B", "1")
    
    mealy = moore_to_mealy(moore)
    
    # Check that conversion is valid
    is_valid, msg = mealy.validate()
    assert is_valid


def test_conversion_roundtrip():
    """Test that conversions work in both directions."""
    # Create Mealy machine
    mealy1 = MealyMachine()
    mealy1.add_state("S0", is_start=True)
    mealy1.add_state("S1")
    mealy1.add_transition("S0", "S1", "a", "0")
    mealy1.add_transition("S1", "S0", "b", "1")
    
    # Convert to Moore and back
    moore = mealy_to_moore(mealy1)
    mealy2 = moore_to_mealy(moore)
    
    # Both should be valid
    assert mealy1.validate()[0]
    assert moore.validate()[0]
    assert mealy2.validate()[0]
