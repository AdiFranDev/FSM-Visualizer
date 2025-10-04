"""DFA minimization using Hopcroft's algorithm."""

from typing import Set, Dict, List, Tuple
from models.dfa import DFA


def minimize_dfa(dfa: DFA) -> DFA:
    """
    Minimize a DFA using Hopcroft's algorithm.
    
    Args:
        dfa: The DFA to minimize
        
    Returns:
        Minimized DFA
    """
    # Remove unreachable states first
    reachable = find_reachable_states(dfa)
    
    # Initialize partition: accepting and non-accepting states
    partitions: List[Set[str]] = []
    
    accept_states = dfa.accept_states & reachable
    non_accept_states = reachable - dfa.accept_states
    
    if accept_states:
        partitions.append(accept_states)
    if non_accept_states:
        partitions.append(non_accept_states)
    
    # Refine partitions
    changed = True
    while changed:
        changed = False
        new_partitions = []
        
        for partition in partitions:
            # Try to split this partition
            split = split_partition(dfa, partition, partitions)
            
            if len(split) > 1:
                changed = True
                new_partitions.extend(split)
            else:
                new_partitions.append(partition)
        
        partitions = new_partitions
    
    # Build minimized DFA
    return build_minimized_dfa(dfa, partitions)


def find_reachable_states(dfa: DFA) -> Set[str]:
    """Find all states reachable from the start state."""
    reachable = set()
    stack = [dfa.start_state]
    
    while stack:
        state = stack.pop()
        if state in reachable:
            continue
        
        reachable.add(state)
        
        for symbol in dfa.alphabet:
            next_state = dfa.get_transition(state, symbol)
            if next_state and next_state not in reachable:
                stack.append(next_state)
    
    return reachable


def split_partition(dfa: DFA, partition: Set[str], all_partitions: List[Set[str]]) -> List[Set[str]]:
    """Try to split a partition based on transitions."""
    if len(partition) <= 1:
        return [partition]
    
    # Group states by their transition signatures
    signatures: Dict[Tuple, Set[str]] = {}
    
    for state in partition:
        # Create signature: which partition each symbol leads to
        sig = []
        for symbol in sorted(dfa.alphabet):
            next_state = dfa.get_transition(state, symbol)
            
            # Find which partition the next state belongs to
            partition_idx = -1
            for i, p in enumerate(all_partitions):
                if next_state in p:
                    partition_idx = i
                    break
            
            sig.append(partition_idx)
        
        sig_tuple = tuple(sig)
        if sig_tuple not in signatures:
            signatures[sig_tuple] = set()
        signatures[sig_tuple].add(state)
    
    return list(signatures.values())


def build_minimized_dfa(original_dfa: DFA, partitions: List[Set[str]]) -> DFA:
    """Build a new DFA from partitions."""
    minimized = DFA()
    
    # Create mapping from old states to partition representatives
    state_map: Dict[str, str] = {}
    partition_reps: Dict[int, str] = {}
    
    for i, partition in enumerate(partitions):
        # Use first state as representative
        rep = f"q{i}"
        partition_reps[i] = rep
        minimized.add_state(rep)
        
        for state in partition:
            state_map[state] = rep
            
            # Check if this is an accept state
            if state in original_dfa.accept_states:
                minimized.accept_states.add(rep)
    
    # Set start state
    minimized.start_state = state_map[original_dfa.start_state]
    
    # Add transitions (one per partition)
    added_transitions = set()
    for partition in partitions:
        rep_state = state_map[next(iter(partition))]
        
        # Use any state from partition to determine transitions
        sample_state = next(iter(partition))
        
        for symbol in original_dfa.alphabet:
            next_state = original_dfa.get_transition(sample_state, symbol)
            
            if next_state:
                next_rep = state_map[next_state]
                trans_key = (rep_state, symbol)
                
                if trans_key not in added_transitions:
                    minimized.add_transition(rep_state, next_rep, symbol)
                    added_transitions.add(trans_key)
    
    return minimized