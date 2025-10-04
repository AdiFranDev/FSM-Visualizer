"""Regular expression parser."""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class RegexNode:
    """AST node for regular expressions."""
    type: str  # 'CHAR', 'STAR', 'PLUS', 'CONCAT', 'OR', 'EPSILON'
    value: Optional[str] = None
    left: Optional['RegexNode'] = None
    right: Optional['RegexNode'] = None


class RegexParser:
    """Parse regular expressions into AST."""
    
    def __init__(self, regex: str):
        self.regex = regex.replace(' ', '')  # Remove spaces
        self.pos = 0
    
    def peek(self) -> Optional[str]:
        """Peek at current character without consuming."""
        if self.pos < len(self.regex):
            return self.regex[self.pos]
        return None
    
    def consume(self) -> Optional[str]:
        """Consume and return current character."""
        if self.pos < len(self.regex):
            char = self.regex[self.pos]
            self.pos += 1
            return char
        return None
    
    def parse(self) -> RegexNode:
        """Parse the entire regex."""
        return self.parse_or()
    
    def parse_or(self) -> RegexNode:
        """Parse OR expressions (lowest precedence)."""
        left = self.parse_concat()
        
        while self.peek() == '|':
            self.consume()  # consume '|'
            right = self.parse_concat()
            left = RegexNode(type='OR', left=left, right=right)
        
        return left
    
    def parse_concat(self) -> RegexNode:
        """Parse concatenation (implicit operator)."""
        nodes = []
        
        while self.peek() and self.peek() not in ')|':
            nodes.append(self.parse_star())
        
        if not nodes:
            return RegexNode(type='EPSILON')
        
        # Build left-associative concat tree
        result = nodes[0]
        for node in nodes[1:]:
            result = RegexNode(type='CONCAT', left=result, right=node)
        
        return result
    
    def parse_star(self) -> RegexNode:
        """Parse star and plus operators (highest precedence)."""
        node = self.parse_base()
        
        char = self.peek()
        while char and char in '*+':
            op = self.consume()
            if op == '*':
                node = RegexNode(type='STAR', left=node)
            else:  # '+'
                node = RegexNode(type='PLUS', left=node)
            char = self.peek()
        
        return node
    
    def parse_base(self) -> RegexNode:
        """Parse base expressions (characters, epsilon, parentheses)."""
        char = self.peek()
        
        if char == '(':
            self.consume()  # consume '('
            node = self.parse_or()
            if self.peek() == ')':
                self.consume()  # consume ')'
            else:
                raise ValueError(f"Expected ')' at position {self.pos}")
            return node
        
        elif char == 'ε' or (char == '\\' and self.pos + 1 < len(self.regex) and self.regex[self.pos + 1] == 'e'):
            if char == '\\':
                self.consume()  # consume '\'
                self.consume()  # consume 'e'
            else:
                self.consume()  # consume 'ε'
            return RegexNode(type='EPSILON')
        
        elif char and char not in ')|*+':
            self.consume()
            return RegexNode(type='CHAR', value=char)
        
        else:
            raise ValueError(f"Unexpected character '{char}' at position {self.pos}")


def parse_regex(regex: str) -> RegexNode:
    """
    Parse a regular expression string into an AST.
    
    Supported operators:
    - * (Kleene star)
    - + (one or more)
    - | (alternation/OR)
    - () (grouping)
    - ε or \\e (epsilon)
    - implicit concatenation
    
    Example: "(a|b)*abb" -> AST
    """
    if not regex:
        return RegexNode(type='EPSILON')
    
    parser = RegexParser(regex)
    return parser.parse()
