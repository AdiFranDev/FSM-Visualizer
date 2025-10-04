"""Parsers package."""

from parsers.json_parser import parse_json_automaton
from parsers.text_parser import parse_text_automaton

__all__ = ['parse_json_automaton', 'parse_text_automaton']