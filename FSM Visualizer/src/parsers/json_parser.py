"""JSON parser for automaton definitions."""

import json
from typing import Dict, Any
from models.dfa import DFA
from models.nfa import NFA, EpsilonNFA


def parse_json_automaton(json_text: str):
    """Parse JSON automaton definition.
    
    Args:
        json_text: JSON string containing automaton definition
        
    Returns:
        Automaton object (DFA, NFA, or EpsilonNFA)
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    automaton_type = data.get("type", "DFA").upper()
    
    if automaton_type == "DFA":
        return parse_dfa(data)
    elif automaton_type == "NFA":
        return parse_nfa(data)
    elif automaton_type == "ENFA" or automaton_type == "EPSILON-NFA":
        return parse_epsilon_nfa(data)
    else:
        raise ValueError(f"Unknown automaton type: {automaton_type}")


def parse_dfa(data: Dict[str, Any]) -> DFA:
    """Parse DFA from JSON data."""
    states = set(data["states"])
    alphabet = set(data["alphabet"])
    transitions = {}
    
    for trans in data["transitions"]:
        from_state = trans["from"]
        symbol = trans["symbol"]
        to_state = trans["to"]
        transitions[(from_state, symbol)] = to_state
    
    start_state = data["start_state"]
    accept_states = set(data["accept_states"])
    
    return DFA(states, alphabet, transitions, start_state, accept_states)


def parse_nfa(data: Dict[str, Any]) -> NFA:
    """Parse NFA from JSON data."""
    states = set(data["states"])
    alphabet = set(data["alphabet"])
    transitions = {}
    
    for trans in data["transitions"]:
        from_state = trans["from"]
        symbol = trans["symbol"]
        to_state = trans["to"]
        
        key = (from_state, symbol)
        if key not in transitions:
            transitions[key] = set()
        transitions[key].add(to_state)
    
    start_state = data["start_state"]
    accept_states = set(data["accept_states"])
    
    return NFA(states, alphabet, transitions, start_state, accept_states)


def parse_epsilon_nfa(data: Dict[str, Any]) -> EpsilonNFA:
    """Parse ε-NFA from JSON data."""
    states = set(data["states"])
    alphabet = set(data["alphabet"])
    transitions = {}
    
    for trans in data["transitions"]:
        from_state = trans["from"]
        symbol = trans.get("symbol", "ε")  # Default to epsilon if not specified
        to_state = trans["to"]
        
        key = (from_state, symbol)
        if key not in transitions:
            transitions[key] = set()
        transitions[key].add(to_state)
    
    start_state = data["start_state"]
    accept_states = set(data["accept_states"])
    
    return EpsilonNFA(states, alphabet, transitions, start_state, accept_states)