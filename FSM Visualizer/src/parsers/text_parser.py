"""Text parser for automaton definitions."""

from models.dfa import DFA
from models.nfa import NFA, EpsilonNFA


def parse_text_automaton(text: str):
    """Parse text-based automaton definition.
    
    Expected format:
        type: DFA|NFA|ENFA
        states: q0, q1, q2
        alphabet: a, b
        start: q0
        accept: q2
        transitions:
        q0, a -> q1
        q1, b -> q2
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    automaton_type = None
    states = set()
    alphabet = set()
    start_state = None
    accept_states = set()
    transitions = {}
    
    in_transitions = False
    
    for line in lines:
        if line.startswith('#'):  # Comment
            continue
            
        if line.lower().startswith('type:'):
            automaton_type = line.split(':', 1)[1].strip().upper()
        elif line.lower().startswith('states:'):
            states = set(s.strip() for s in line.split(':', 1)[1].split(','))
        elif line.lower().startswith('alphabet:'):
            alphabet = set(s.strip() for s in line.split(':', 1)[1].split(','))
        elif line.lower().startswith('start:'):
            start_state = line.split(':', 1)[1].strip()
        elif line.lower().startswith('accept:'):
            accept_states = set(s.strip() for s in line.split(':', 1)[1].split(','))
        elif line.lower().startswith('transitions:'):
            in_transitions = True
        elif in_transitions and '->' in line:
            parts = line.split('->')
            from_part = parts[0].strip()
            to_state = parts[1].strip()
            
            if ',' in from_part:
                from_state, symbol = [p.strip() for p in from_part.split(',', 1)]
            else:
                raise ValueError(f"Invalid transition format: {line}")
            
            if automaton_type == 'DFA':
                transitions[(from_state, symbol)] = to_state
            else:  # NFA or ENFA
                key = (from_state, symbol)
                if key not in transitions:
                    transitions[key] = set()
                transitions[key].add(to_state)
    
    if not automaton_type:
        raise ValueError("Automaton type not specified")
    
    if automaton_type == 'DFA':
        return DFA(states, alphabet, transitions, start_state, accept_states)
    elif automaton_type == 'NFA':
        return NFA(states, alphabet, transitions, start_state, accept_states)
    elif automaton_type in ('ENFA', 'EPSILON-NFA'):
        return EpsilonNFA(states, alphabet, transitions, start_state, accept_states)
    else:
        raise ValueError(f"Unknown automaton type: {automaton_type}")