"""Mealy and Moore machine implementations."""

from typing import Dict, List, Tuple, Optional
from .automaton import Automaton, State


class MealyMachine(Automaton):
    """Mealy machine (output depends on transitions)."""
    
    def __init__(self):
        super().__init__()
        self.output_alphabet: set[str] = set()
        self._transition_table: Dict[Tuple[str, str], Tuple[str, str]] = {}  # (state, input) -> (next_state, output)
    
    def add_transition(self, from_state: str, to_state: str, symbol: str, output: Optional[str] = None):
        """Add a Mealy transition with output."""
        if output is None:
            raise ValueError("Mealy machine transitions must have output")
        
        super().add_transition(from_state, to_state, symbol, output)
        self._transition_table[(from_state, symbol)] = (to_state, output)
        self.output_alphabet.add(output)
    
    def get_next_state_and_output(self, current_state: str, symbol: str) -> Optional[Tuple[str, str]]:
        """Get next state and output for given state and input."""
        return self._transition_table.get((current_state, symbol))
    
    def process_input(self, input_string: str) -> Tuple[bool, List[str]]:
        """
        Process input and return (success, output_sequence).
        Success is False if transition is undefined at any point.
        """
        if self.start_state is None:
            return False, []
        
        current_state = self.start_state
        outputs = []
        
        for symbol in input_string:
            result = self.get_next_state_and_output(current_state, symbol)
            if result is None:
                return False, outputs
            
            next_state, output = result
            outputs.append(output)
            current_state = next_state
        
        return True, outputs
    
    def simulate_step_by_step(self, input_string: str) -> List[Tuple[str, str, str, str]]:
        """
        Simulate step by step.
        Returns list of (current_state, input_symbol, output, next_state) tuples.
        """
        if self.start_state is None:
            return []
        
        steps = []
        current_state = self.start_state
        
        for symbol in input_string:
            result = self.get_next_state_and_output(current_state, symbol)
            if result is None:
                steps.append((current_state, symbol, "ERROR", "ERROR"))
                break
            
            next_state, output = result
            steps.append((current_state, symbol, output, next_state))
            current_state = next_state
        
        return steps
    
    def accepts(self, input_string: str) -> bool:
        """Mealy machines don't accept/reject, they just produce output."""
        success, _ = self.process_input(input_string)
        return success
    
    def get_transition_function(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Return transition function with outputs."""
        result = {}
        
        for (from_state, symbol), (to_state, output) in self._transition_table.items():
            if from_state not in result:
                result[from_state] = {}
            result[from_state][symbol] = {'next_state': to_state, 'output': output}
        
        return result


class MooreMachine(Automaton):
    """Moore machine (output depends on states)."""
    
    def __init__(self):
        super().__init__()
        self.output_alphabet: set[str] = set()
        self.state_outputs: Dict[str, str] = {}  # state -> output
        self._transition_table: Dict[Tuple[str, str], str] = {}  # (state, input) -> next_state
    
    def add_state(self, name: str, is_accept: bool = False, is_start: bool = False) -> 'State':
        """Add state (output will be set separately)."""
        return super().add_state(name, is_accept, is_start)
    
    def set_state_output(self, state: str, output: str):
        """Set the output for a state."""
        if state not in self.states:
            raise ValueError(f"State '{state}' does not exist")
        
        self.state_outputs[state] = output
        self.output_alphabet.add(output)
    
    def add_transition(self, from_state: str, to_state: str, symbol: str, output: Optional[str] = None):
        """Add a Moore transition (output is ignored, attached to states)."""
        super().add_transition(from_state, to_state, symbol, None)
        self._transition_table[(from_state, symbol)] = to_state
    
    def get_next_state(self, current_state: str, symbol: str) -> Optional[str]:
        """Get next state for given state and input."""
        return self._transition_table.get((current_state, symbol))
    
    def get_state_output(self, state: str) -> Optional[str]:
        """Get output for a given state."""
        return self.state_outputs.get(state)
    
    def process_input(self, input_string: str) -> Tuple[bool, List[str]]:
        """
        Process input and return (success, output_sequence).
        Output sequence includes initial state output.
        """
        if self.start_state is None:
            return False, []
        
        current_state = self.start_state
        outputs = [self.state_outputs.get(current_state, "")]
        
        for symbol in input_string:
            next_state = self.get_next_state(current_state, symbol)
            if next_state is None:
                return False, outputs
            
            current_state = next_state
            outputs.append(self.state_outputs.get(current_state, ""))
        
        return True, outputs
    
    def simulate_step_by_step(self, input_string: str) -> List[Tuple[str, str, str, str]]:
        """
        Simulate step by step.
        Returns list of (current_state, input_symbol, next_state, output) tuples.
        """
        if self.start_state is None:
            return []
        
        steps = []
        current_state = self.start_state
        
        for symbol in input_string:
            next_state = self.get_next_state(current_state, symbol)
            if next_state is None:
                steps.append((current_state, symbol, "ERROR", "ERROR"))
                break
            
            output = self.state_outputs.get(next_state, "")
            steps.append((current_state, symbol, next_state, output))
            current_state = next_state
        
        return steps
    
    def accepts(self, input_string: str) -> bool:
        """Moore machines don't accept/reject, they just produce output."""
        success, _ = self.process_input(input_string)
        return success
    
    def get_transition_function(self) -> Dict[str, Dict[str, str]]:
        """Return transition function."""
        result = {}
        
        for (from_state, symbol), to_state in self._transition_table.items():
            if from_state not in result:
                result[from_state] = {}
            result[from_state][symbol] = to_state
        
        return result
    
    def validate(self) -> tuple[bool, str]:
        """Validate Moore machine (all states must have outputs)."""
        is_valid, msg = super().validate()
        if not is_valid:
            return False, msg
        
        for state_name in self.states:
            if state_name not in self.state_outputs:
                return False, f"State '{state_name}' has no output defined"
        
        return True, "Valid Moore machine"
