"""Base classes for automaton models."""

from dataclasses import dataclass, field
from typing import Set, Dict, List, Optional, Any
from abc import ABC, abstractmethod


@dataclass
class State:
    """Represents a state in an automaton."""
    name: str
    is_accept: bool = False
    is_start: bool = False
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, State):
            return self.name == other.name
        return False
    
    def __str__(self):
        return self.name


@dataclass
class Transition:
    """Represents a transition in an automaton."""
    from_state: str
    to_state: str
    symbol: str
    output: Optional[str] = None  # For Mealy/Moore machines
    
    def __hash__(self):
        return hash((self.from_state, self.to_state, self.symbol))


class Automaton(ABC):
    """Abstract base class for all automaton types."""
    
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.alphabet: Set[str] = set()
        self.start_state: Optional[str] = None
        self.accept_states: Set[str] = set()
        self.transitions: List[Transition] = []
    
    def add_state(self, name: str, is_accept: bool = False, is_start: bool = False) -> State:
        """Add a state to the automaton."""
        state = State(name, is_accept, is_start)
        self.states[name] = state
        
        if is_accept:
            self.accept_states.add(name)
        if is_start:
            self.start_state = name
        
        return state
    
    def add_transition(self, from_state: str, to_state: str, symbol: str, output: Optional[str] = None):
        """Add a transition to the automaton."""
        if symbol != 'ε':  # Don't add epsilon to alphabet
            self.alphabet.add(symbol)
        
        transition = Transition(from_state, to_state, symbol, output)
        self.transitions.append(transition)
    
    @abstractmethod
    def accepts(self, input_string: str) -> bool:
        """Check if the automaton accepts the input string."""
        pass
    
    @abstractmethod
    def get_transition_function(self) -> Dict[str, Any]:
        """Return the transition function in a structured format."""
        pass
    
    def validate(self) -> tuple[bool, str]:
        """Validate the automaton structure."""
        if not self.states:
            return False, "No states defined"
        
        if self.start_state is None:
            return False, "No start state defined"
        
        if self.start_state not in self.states:
            return False, f"Start state '{self.start_state}' not in states"
        
        # Check all transitions reference valid states
        for trans in self.transitions:
            if trans.from_state not in self.states:
                return False, f"Transition from undefined state '{trans.from_state}'"
            if trans.to_state not in self.states:
                return False, f"Transition to undefined state '{trans.to_state}'"
        
        return True, "Valid"
    
    def get_state_count(self) -> int:
        """Return the number of states."""
        return len(self.states)
    
    def get_transition_count(self) -> int:
        """Return the number of transitions."""
        return len(self.transitions)
