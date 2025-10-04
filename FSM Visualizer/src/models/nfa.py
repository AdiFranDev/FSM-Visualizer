"""Non-deterministic Finite Automaton (NFA) and ε-NFA implementation."""

from typing import Dict, Set, List, Tuple, Optional
from collections import defaultdict, deque
from .automaton import Automaton


class NFA(Automaton):
    """Non-deterministic Finite Automaton."""
    
    def __init__(self):
        super().__init__()
        self._transition_table: Dict[Tuple[str, str], Set[str]] = defaultdict(set)
    
    def add_transition(self, from_state: str, to_state: str, symbol: str, output: Optional[str] = None):
        """Add a transition (can be non-deterministic)."""
        super().add_transition(from_state, to_state, symbol, output)
        self._transition_table[(from_state, symbol)].add(to_state)
    
    def get_next_states(self, current_state: str, symbol: str) -> Set[str]:
        """Get all possible next states for a given state and symbol."""
        return self._transition_table.get((current_state, symbol), set())
    
    def accepts(self, input_string: str) -> bool:
        """Check if the NFA accepts the input string."""
        if self.start_state is None:
            return False
        
        current_states = {self.start_state}
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states.update(self.get_next_states(state, symbol))
            
            if not next_states:
                return False
            
            current_states = next_states
        
        return bool(current_states & self.accept_states)
    
    def simulate_step_by_step(self, input_string: str) -> List[Tuple[Set[str], str, Set[str]]]:
        """
        Simulate the NFA step by step.
        Returns a list of (current_states, symbol, next_states) tuples.
        """
        if self.start_state is None:
            return []
        
        steps = []
        current_states = {self.start_state}
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states.update(self.get_next_states(state, symbol))
            
            steps.append((current_states.copy(), symbol, next_states.copy()))
            
            if not next_states:
                break
            
            current_states = next_states
        
        return steps
    
    def get_transition_function(self) -> Dict[str, Dict[str, List[str]]]:
        """Return the transition function as a nested dictionary."""
        result = {}
        
        for (from_state, symbol), to_states in self._transition_table.items():
            if from_state not in result:
                result[from_state] = {}
            result[from_state][symbol] = list(to_states)
        
        return result


class EpsilonNFA(NFA):
    """ε-NFA (NFA with epsilon transitions)."""
    
    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """Compute the epsilon closure of a set of states."""
        closure = set(states)
        queue = deque(states)
        
        while queue:
            state = queue.popleft()
            epsilon_transitions = self.get_next_states(state, 'ε')
            
            for next_state in epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    queue.append(next_state)
        
        return closure
    
    def accepts(self, input_string: str) -> bool:
        """Check if the ε-NFA accepts the input string."""
        if self.start_state is None:
            return False
        
        # Start with epsilon closure of start state
        current_states = self.epsilon_closure({self.start_state})
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                # Get states reachable by the symbol
                symbol_states = self.get_next_states(state, symbol)
                next_states.update(symbol_states)
            
            if not next_states:
                return False
            
            # Apply epsilon closure to the result
            current_states = self.epsilon_closure(next_states)
        
        return bool(current_states & self.accept_states)
    
    def simulate_step_by_step(self, input_string: str) -> List[Tuple[Set[str], str, Set[str]]]:
        """
        Simulate the ε-NFA step by step with epsilon closures.
        Returns a list of (current_states_with_ε, symbol, next_states_with_ε) tuples.
        """
        if self.start_state is None:
            return []
        
        steps = []
        current_states = self.epsilon_closure({self.start_state})
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states.update(self.get_next_states(state, symbol))
            
            next_states_with_epsilon = self.epsilon_closure(next_states)
            steps.append((current_states.copy(), symbol, next_states_with_epsilon.copy()))
            
            if not next_states_with_epsilon:
                break
            
            current_states = next_states_with_epsilon
        
        return steps
    
    def get_all_epsilon_transitions(self) -> List[Tuple[str, str]]:
        """Get all epsilon transitions as (from_state, to_state) pairs."""
        epsilon_trans = []
        for trans in self.transitions:
            if trans.symbol == 'ε':
                epsilon_trans.append((trans.from_state, trans.to_state))
        return epsilon_trans
