"""Deterministic Finite Automaton (DFA) implementation."""

from typing import Dict, Optional, List, Tuple
from .automaton import Automaton


class DFA(Automaton):
    """Deterministic Finite Automaton."""
    
    def __init__(self):
        super().__init__()
        self._transition_table: Dict[Tuple[str, str], str] = {}
    
    def add_transition(self, from_state: str, to_state: str, symbol: str, output: Optional[str] = None):
        """Add a transition (must be deterministic)."""
        key = (from_state, symbol)
        if key in self._transition_table:
            raise ValueError(f"DFA transition already exists: {from_state} --{symbol}--> (multiple states)")
        
        super().add_transition(from_state, to_state, symbol, output)
        self._transition_table[key] = to_state
    
    def get_next_state(self, current_state: str, symbol: str) -> Optional[str]:
        """Get the next state for a given state and symbol."""
        return self._transition_table.get((current_state, symbol))
    
    def accepts(self, input_string: str) -> bool:
        """Check if the DFA accepts the input string."""
        if self.start_state is None:
            return False
        
        current_state = self.start_state
        
        for symbol in input_string:
            next_state = self.get_next_state(current_state, symbol)
            if next_state is None:
                return False
            current_state = next_state
        
        return current_state in self.accept_states
    
    def simulate_step_by_step(self, input_string: str) -> List[Tuple[str, str, str]]:
        """
        Simulate the DFA step by step.
        Returns a list of (current_state, symbol, next_state) tuples.
        """
        if self.start_state is None:
            return []
        
        steps = []
        current_state = self.start_state
        
        for symbol in input_string:
            next_state = self.get_next_state(current_state, symbol)
            if next_state is None:
                steps.append((current_state, symbol, "REJECT"))
                break
            steps.append((current_state, symbol, next_state))
            current_state = next_state
        
        return steps
    
    def get_transition_function(self) -> Dict[str, Dict[str, str]]:
        """Return the transition function as a nested dictionary."""
        result = {}
        
        for (from_state, symbol), to_state in self._transition_table.items():
            if from_state not in result:
                result[from_state] = {}
            result[from_state][symbol] = to_state
        
        return result
    
    def validate(self) -> tuple[bool, str]:
        """Validate DFA-specific properties."""
        is_valid, msg = super().validate()
        if not is_valid:
            return False, msg
        
        # Check determinism: each (state, symbol) has at most one transition
        seen = set()
        for trans in self.transitions:
            key = (trans.from_state, trans.symbol)
            if key in seen:
                return False, f"Non-deterministic transition: {trans.from_state} --{trans.symbol}-->"
            seen.add(key)
        
        return True, "Valid DFA"
    
    def is_complete(self) -> bool:
        """Check if the DFA is complete (all transitions defined)."""
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self._transition_table:
                    return False
        return True
