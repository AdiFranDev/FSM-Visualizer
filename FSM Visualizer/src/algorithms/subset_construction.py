"""Subset construction algorithm for converting NFA to DFA."""

from typing import Set, Dict, Tuple, FrozenSet
from models.nfa import NFA, EpsilonNFA
from models.dfa import DFA


def epsilon_closure(nfa: EpsilonNFA, states: Set[str]) -> Set[str]:
    """
    Compute the epsilon closure of a set of states.
    
    Args:
        nfa: The epsilon-NFA
        states: Set of states
        
    Returns:
        Set of states reachable via epsilon transitions
    """
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        # Get epsilon transitions from this state
        for next_state in nfa.get_transitions(state, 'ε'):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    
    return closure


def epsilon_nfa_to_nfa(enfa: EpsilonNFA) -> NFA:
    """
    Convert an epsilon-NFA to an NFA (removing epsilon transitions).
    
    Args:
        enfa: The epsilon-NFA to convert
        
    Returns:
        Equivalent NFA without epsilon transitions
    """
    nfa = NFA()
    
    # Add all states
    for state in enfa.states:
        nfa.add_state(state)
    
    # Set start state
    nfa.start_state = enfa.start_state
    
    # For each state, compute epsilon closure and add transitions
    for state in enfa.states:
        e_closure = epsilon_closure(enfa, {state})
        
        # Check if any state in epsilon closure is accepting
        if any(s in enfa.accept_states for s in e_closure):
            nfa.accept_states.add(state)
        
        # Add transitions for each symbol in alphabet (excluding epsilon)
        for symbol in enfa.alphabet:
            if symbol == 'ε':
                continue
                
            # Get all states reachable by this symbol from epsilon closure
            next_states = set()
            for s in e_closure:
                next_states.update(enfa.get_transitions(s, symbol))
            
            # Compute epsilon closure of the result
            if next_states:
                final_states = epsilon_closure(enfa, next_states)
                for target in final_states:
                    nfa.add_transition(state, target, symbol)
    
    return nfa


def nfa_to_dfa(nfa: NFA) -> DFA:
    """
    Convert an NFA to a DFA using subset construction.
    
    Args:
        nfa: The NFA to convert
        
    Returns:
        Equivalent DFA
    """
    dfa = DFA()
    
    # Start with the NFA's start state as a singleton set
    start_state_set = frozenset({nfa.start_state})
    state_map: Dict[FrozenSet[str], str] = {}
    state_counter = [0]
    
    def get_dfa_state(nfa_states: FrozenSet[str]) -> str:
        """Get or create DFA state for a set of NFA states."""
        if nfa_states not in state_map:
            state_counter[0] += 1
            dfa_state = f"q{state_counter[0]}"
            state_map[nfa_states] = dfa_state
            
            # Add state to DFA
            dfa.add_state(dfa_state)
            
            # Check if this is an accept state
            if any(s in nfa.accept_states for s in nfa_states):
                dfa.accept_states.add(dfa_state)
        
        return state_map[nfa_states]
    
    # Create start state
    dfa.start_state = get_dfa_state(start_state_set)
    
    # Queue of state sets to process
    queue = [start_state_set]
    processed = set()
    
    while queue:
        current_set = queue.pop(0)
        
        if current_set in processed:
            continue
        processed.add(current_set)
        
        current_dfa_state = get_dfa_state(current_set)
        
        # For each symbol in alphabet
        for symbol in nfa.alphabet:
            # Compute the set of states reachable by this symbol
            next_states = set()
            for nfa_state in current_set:
                next_states.update(nfa.get_transitions(nfa_state, symbol))
            
            if next_states:
                next_state_set = frozenset(next_states)
                next_dfa_state = get_dfa_state(next_state_set)
                
                # Add transition to DFA
                dfa.add_transition(current_dfa_state, next_dfa_state, symbol)
                
                # Add to queue if not processed
                if next_state_set not in processed:
                    queue.append(next_state_set)
    
    return dfa