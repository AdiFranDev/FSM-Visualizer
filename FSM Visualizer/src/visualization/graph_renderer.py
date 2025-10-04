"""Render automata using Graphviz."""

from typing import Union, Optional
import graphviz
from ..models.automaton import Automaton
from ..models.pda import PDA
from ..models.mealy_moore import MealyMachine, MooreMachine


def render_automaton(automaton: Automaton, title: str = "Automaton") -> graphviz.Digraph:
    """
    Render an automaton as a Graphviz graph.
    
    Args:
        automaton: The automaton to render
        title: Title for the graph
    
    Returns:
        Graphviz Digraph object
    """
    dot = graphviz.Digraph(comment=title)
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    
    # Add invisible start node
    dot.node('__start__', '', shape='none', width='0', height='0')
    
    # Add states
    for state_name, state in automaton.states.items():
        attrs = {}
        
        if state.is_accept:
            attrs['shape'] = 'doublecircle'
        
        # For Moore machines, add output to state label
        if isinstance(automaton, MooreMachine):
            output = automaton.get_state_output(state_name)
            label = f"{state_name}\n{output}" if output else state_name
            attrs['label'] = label
        
        dot.node(state_name, **attrs)
        
        # Add start arrow
        if state.is_start:
            dot.edge('__start__', state_name)
    
    # Group transitions by (from, to) for combined labels
    transition_labels = {}
    
    for trans in automaton.transitions:
        key = (trans.from_state, trans.to_state)
        
        if isinstance(automaton, MealyMachine):
            label = f"{trans.symbol}/{trans.output}"
        elif isinstance(automaton, PDA):
            # PDA transitions already have formatted labels
            label = trans.symbol
        else:
            label = trans.symbol
        
        if key not in transition_labels:
            transition_labels[key] = []
        transition_labels[key].append(label)
    
    # Add transitions with combined labels
    for (from_state, to_state), labels in transition_labels.items():
        combined_label = ', '.join(labels)
        dot.edge(from_state, to_state, label=combined_label)
    
    return dot


def export_graph(automaton: Automaton, filepath: str, format: str = 'png', title: str = "Automaton"):
    """
    Export automaton graph to file.
    
    Args:
        automaton: The automaton to export
        filepath: Output file path (without extension)
        format: Output format ('png', 'svg', 'pdf', etc.)
        title: Graph title
    """
    dot = render_automaton(automaton, title)
    dot.render(filepath, format=format, cleanup=True)
