"""Simulation logic for automata."""

from dataclasses import dataclass
from typing import List, Union, Any
from ..models.automaton import Automaton
from ..models.dfa import DFA
from ..models.nfa import NFA, EpsilonNFA
from ..models.pda import PDA, PDAConfiguration
from ..models.mealy_moore import MealyMachine, MooreMachine


@dataclass
class SimulationResult:
    """Result of automaton simulation."""
    accepted: bool
    steps: List[Any]
    final_output: List[str] = None  # For Mealy/Moore machines


def simulate_automaton(automaton: Automaton, input_string: str) -> SimulationResult:
    """
    Simulate an automaton on an input string.
    
    Returns simulation result with step-by-step execution.
    """
    if isinstance(automaton, DFA):
        return _simulate_dfa(automaton, input_string)
    elif isinstance(automaton, EpsilonNFA):
        return _simulate_epsilon_nfa(automaton, input_string)
    elif isinstance(automaton, NFA):
        return _simulate_nfa(automaton, input_string)
    elif isinstance(automaton, PDA):
        return _simulate_pda(automaton, input_string)
    elif isinstance(automaton, MealyMachine):
        return _simulate_mealy(automaton, input_string)
    elif isinstance(automaton, MooreMachine):
        return _simulate_moore(automaton, input_string)
    else:
        raise ValueError(f"Unknown automaton type: {type(automaton)}")


def _simulate_dfa(dfa: DFA, input_string: str) -> SimulationResult:
    """Simulate DFA."""
    steps = dfa.simulate_step_by_step(input_string)
    accepted = dfa.accepts(input_string)
    return SimulationResult(accepted=accepted, steps=steps)


def _simulate_nfa(nfa: NFA, input_string: str) -> SimulationResult:
    """Simulate NFA."""
    steps = nfa.simulate_step_by_step(input_string)
    accepted = nfa.accepts(input_string)
    return SimulationResult(accepted=accepted, steps=steps)


def _simulate_epsilon_nfa(enfa: EpsilonNFA, input_string: str) -> SimulationResult:
    """Simulate ε-NFA."""
    steps = enfa.simulate_step_by_step(input_string)
    accepted = enfa.accepts(input_string)
    return SimulationResult(accepted=accepted, steps=steps)


def _simulate_pda(pda: PDA, input_string: str) -> SimulationResult:
    """Simulate PDA."""
    steps = pda.simulate_step_by_step(input_string)
    accepted = pda.accepts(input_string)
    return SimulationResult(accepted=accepted, steps=steps)


def _simulate_mealy(mealy: MealyMachine, input_string: str) -> SimulationResult:
    """Simulate Mealy machine."""
    steps = mealy.simulate_step_by_step(input_string)
    success, outputs = mealy.process_input(input_string)
    return SimulationResult(accepted=success, steps=steps, final_output=outputs)


def _simulate_moore(moore: MooreMachine, input_string: str) -> SimulationResult:
    """Simulate Moore machine."""
    steps = moore.simulate_step_by_step(input_string)
    success, outputs = moore.process_input(input_string)
    return SimulationResult(accepted=success, steps=steps, final_output=outputs)
