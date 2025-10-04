"""Pushdown Automaton (PDA) implementation."""

from typing import Dict, Set, List, Tuple, Optional
from dataclasses import dataclass
from .automaton import Automaton


@dataclass
class PDATransition:
    """Represents a PDA transition with stack operations."""
    from_state: str
    to_state: str
    input_symbol: str  # Can be 'ε' for epsilon
    stack_pop: str     # Symbol to pop from stack
    stack_push: List[str]  # Symbols to push (in order, top first)
    
    def __str__(self):
        push_str = ''.join(self.stack_push) if self.stack_push else 'ε'
        return f"{self.from_state} --{self.input_symbol},{self.stack_pop}/{push_str}--> {self.to_state}"


@dataclass
class PDAConfiguration:
    """Represents a configuration (state, remaining input, stack)."""
    state: str
    remaining_input: str
    stack: List[str]  # Top of stack at index 0
    
    def __str__(self):
        stack_str = ''.join(self.stack) if self.stack else '⊥'
        return f"({self.state}, {self.remaining_input or 'ε'}, {stack_str})"


class PDA(Automaton):
    """Pushdown Automaton."""
    
    def __init__(self):
        super().__init__()
        self.stack_alphabet: Set[str] = set()
        self.start_stack_symbol: str = 'Z'  # Default start symbol
        self._pda_transitions: List[PDATransition] = []
    
    def add_pda_transition(self, from_state: str, to_state: str, input_symbol: str,
                          stack_pop: str, stack_push: List[str]):
        """Add a PDA transition with stack operations."""
        # Add to stack alphabet
        self.stack_alphabet.add(stack_pop)
        for symbol in stack_push:
            if symbol != 'ε':
                self.stack_alphabet.add(symbol)
        
        # Add to input alphabet if not epsilon
        if input_symbol != 'ε':
            self.alphabet.add(input_symbol)
        
        transition = PDATransition(from_state, to_state, input_symbol, stack_pop, stack_push)
        self._pda_transitions.append(transition)
        
        # Also add to base transitions for visualization
        label = f"{input_symbol},{stack_pop}/{''.join(stack_push) if stack_push else 'ε'}"
        super().add_transition(from_state, to_state, label)
    
    def get_applicable_transitions(self, state: str, input_symbol: Optional[str],
                                   stack_top: Optional[str]) -> List[PDATransition]:
        """Get all transitions applicable to current configuration."""
        applicable = []
        
        for trans in self._pda_transitions:
            if trans.from_state != state:
                continue
            
            if stack_top is None or trans.stack_pop != stack_top:
                continue
            
            # Transition can read current input or be epsilon
            if trans.input_symbol == input_symbol or trans.input_symbol == 'ε':
                applicable.append(trans)
        
        return applicable
    
    def accepts(self, input_string: str) -> bool:
        """
        Check if PDA accepts by final state.
        Uses BFS to explore all possible computation paths.
        """
        if self.start_state is None:
            return False
        
        # Initial configuration
        initial_config = PDAConfiguration(
            state=self.start_state,
            remaining_input=input_string,
            stack=[self.start_stack_symbol]
        )
        
        # BFS queue
        queue = [initial_config]
        visited = set()
        
        while queue:
            config = queue.pop(0)
            
            # Create a hashable representation
            config_key = (config.state, config.remaining_input, tuple(config.stack))
            if config_key in visited:
                continue
            visited.add(config_key)
            
            # Check acceptance: final state + empty input
            if config.state in self.accept_states and not config.remaining_input:
                return True
            
            # Get current input symbol
            current_symbol = config.remaining_input[0] if config.remaining_input else None
            stack_top = config.stack[0] if config.stack else None
            
            if stack_top is None:
                continue
            
            # Try all applicable transitions
            transitions = self.get_applicable_transitions(config.state, current_symbol, stack_top)
            
            for trans in transitions:
                # Create new configuration
                new_stack = config.stack[1:]  # Pop
                
                # Push new symbols (in reverse order since we push to front)
                for symbol in reversed(trans.stack_push):
                    if symbol != 'ε':
                        new_stack.insert(0, symbol)
                
                # Consume input if not epsilon transition
                new_input = config.remaining_input
                if trans.input_symbol != 'ε' and new_input:
                    new_input = new_input[1:]
                
                new_config = PDAConfiguration(
                    state=trans.to_state,
                    remaining_input=new_input,
                    stack=new_stack
                )
                
                queue.append(new_config)
        
        return False
    
    def simulate_step_by_step(self, input_string: str, max_steps: int = 100) -> List[Tuple[PDAConfiguration, Optional[PDATransition]]]:
        """
        Simulate PDA step by step, returning one possible execution path.
        Returns list of (configuration, transition_taken) pairs.
        """
        if self.start_state is None:
            return []
        
        initial_config = PDAConfiguration(
            state=self.start_state,
            remaining_input=input_string,
            stack=[self.start_stack_symbol]
        )
        
        path = [(initial_config, None)]
        config = initial_config
        
        for _ in range(max_steps):
            # Check if accepted
            if config.state in self.accept_states and not config.remaining_input:
                break
            
            current_symbol = config.remaining_input[0] if config.remaining_input else None
            stack_top = config.stack[0] if config.stack else None
            
            if stack_top is None:
                break
            
            # Get applicable transitions (prefer non-epsilon if available)
            transitions = self.get_applicable_transitions(config.state, current_symbol, stack_top)
            
            if not transitions:
                break
            
            # Pick first applicable transition (in real implementation, might explore all)
            trans = transitions[0]
            
            # Apply transition
            new_stack = config.stack[1:]
            for symbol in reversed(trans.stack_push):
                if symbol != 'ε':
                    new_stack.insert(0, symbol)
            
            new_input = config.remaining_input
            if trans.input_symbol != 'ε' and new_input:
                new_input = new_input[1:]
            
            config = PDAConfiguration(
                state=trans.to_state,
                remaining_input=new_input,
                stack=new_stack
            )
            
            path.append((config, trans))
        
        return path
    
    def get_transition_function(self) -> List[Dict]:
        """Return PDA transitions in structured format."""
        result = []
        for trans in self._pda_transitions:
            result.append({
                'from': trans.from_state,
                'to': trans.to_state,
                'input': trans.input_symbol,
                'pop': trans.stack_pop,
                'push': trans.stack_push
            })
        return result
