"""Thompson's construction algorithm for converting regex to ε-NFA."""

from models.nfa import EpsilonNFA
from typing import List, Union  
from .regex_parser import RegexNode, parse_regex


class ThompsonFragment:
    """Fragment of an NFA during Thompson's construction."""
    
    def __init__(self, start: str, accept: str):
        self.start = start
        self.accept = accept


def thompson_construction(regex: str) -> EpsilonNFA:
    """
    Convert a regular expression to an ε-NFA using Thompson's construction.
    
    Args:
        regex: Regular expression string
    
    Returns:
        EpsilonNFA representing the regex
    """
    ast = parse_regex(regex)
    nfa = EpsilonNFA()
    state_counter = [0]  # Use list to allow mutation in nested function
    
    def new_state() -> str:
        """Generate a new unique state name."""
        state_counter[0] += 1
        return f"q{state_counter[0]}"
    
    def build_fragment(node: RegexNode) -> ThompsonFragment:
        """Recursively build NFA fragment from AST node."""
        
        if node.type == 'EPSILON':
            # ε transition from start to accept
            start = new_state()
            accept = new_state()
            nfa.add_state(start)
            nfa.add_state(accept, is_accept=True)
            nfa.add_transition(start, accept, 'ε')
            return ThompsonFragment(start, accept)
        
        elif node.type == 'CHAR':
            # Single character transition
            start = new_state()
            accept = new_state()
            nfa.add_state(start)
            nfa.add_state(accept, is_accept=True)
            nfa.add_transition(start, accept, node.value)
            return ThompsonFragment(start, accept)
        
        elif node.type == 'CONCAT':
            # Concatenation: connect two fragments
            left_frag = build_fragment(node.left)
            right_frag = build_fragment(node.right)
            
            # Remove accept status from left fragment's accept state
            nfa.states[left_frag.accept].is_accept = False
            nfa.accept_states.discard(left_frag.accept)
            
            # Connect left accept to right start with ε
            nfa.add_transition(left_frag.accept, right_frag.start, 'ε')
            
            return ThompsonFragment(left_frag.start, right_frag.accept)
        
        elif node.type == 'OR':
            # Alternation: create new start and accept states
            left_frag = build_fragment(node.left)
            right_frag = build_fragment(node.right)
            
            start = new_state()
            accept = new_state()
            nfa.add_state(start)
            nfa.add_state(accept, is_accept=True)
            
            # Remove accept status from fragment accept states
            nfa.states[left_frag.accept].is_accept = False
            nfa.states[right_frag.accept].is_accept = False
            nfa.accept_states.discard(left_frag.accept)
            nfa.accept_states.discard(right_frag.accept)
            
            # Connect new start to both fragments
            nfa.add_transition(start, left_frag.start, 'ε')
            nfa.add_transition(start, right_frag.start, 'ε')
            
            # Connect both fragments to new accept
            nfa.add_transition(left_frag.accept, accept, 'ε')
            nfa.add_transition(right_frag.accept, accept, 'ε')
            
            return ThompsonFragment(start, accept)
        
        elif node.type == 'STAR':
            # Kleene star: loop back and allow skip
            inner_frag = build_fragment(node.left)
            
            start = new_state()
            accept = new_state()
            nfa.add_state(start)
            nfa.add_state(accept, is_accept=True)
            
            # Remove accept status from inner fragment
            nfa.states[inner_frag.accept].is_accept = False
            nfa.accept_states.discard(inner_frag.accept)
            
            # Connect: start -> inner_start, start -> accept (skip)
            nfa.add_transition(start, inner_frag.start, 'ε')
            nfa.add_transition(start, accept, 'ε')
            
            # Connect: inner_accept -> inner_start (loop), inner_accept -> accept
            nfa.add_transition(inner_frag.accept, inner_frag.start, 'ε')
            nfa.add_transition(inner_frag.accept, accept, 'ε')
            
            return ThompsonFragment(start, accept)
        
        elif node.type == 'PLUS':
            # One or more: A+ = AA*
            inner_frag = build_fragment(node.left)
            
            start = new_state()
            accept = new_state()
            nfa.add_state(start)
            nfa.add_state(accept, is_accept=True)
            
            # Remove accept status from inner fragment
            nfa.states[inner_frag.accept].is_accept = False
            nfa.accept_states.discard(inner_frag.accept)
            
            # Connect: start -> inner_start (must go through once)
            nfa.add_transition(start, inner_frag.start, 'ε')
            
            # Connect: inner_accept -> inner_start (loop), inner_accept -> accept
            nfa.add_transition(inner_frag.accept, inner_frag.start, 'ε')
            nfa.add_transition(inner_frag.accept, accept, 'ε')
            
            return ThompsonFragment(start, accept)
        
        else:
            raise ValueError(f"Unknown node type: {node.type}")
    
    # Build the complete NFA
    fragment = build_fragment(ast)
    
    # Set start state
    nfa.start_state = fragment.start
    nfa.states[fragment.start].is_start = True
    
    return nfa
