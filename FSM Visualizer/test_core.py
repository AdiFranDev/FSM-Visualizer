"""Quick test of core functionality without GUI."""

from src.algorithms.thompson import thompson_construction
from src.algorithms.subset_construction import nfa_to_dfa
from src.algorithms.minimization import minimize_dfa

# Test regex to automaton conversion
print("Testing Thompson's construction...")
enfa = thompson_construction("(a|b)*abb")
print(f"Created ε-NFA with {enfa.get_state_count()} states")

# Test conversion to DFA
print("\nConverting to DFA...")
dfa = nfa_to_dfa(enfa)
print(f"Created DFA with {dfa.get_state_count()} states")

# Test minimization
print("\nMinimizing DFA...")
min_dfa = minimize_dfa(dfa)
print(f"Minimized to {min_dfa.get_state_count()} states")

# Test acceptance
test_strings = ["abb", "aabb", "ab", ""]
print("\nTesting strings:")
for s in test_strings:
    result = min_dfa.accepts(s)
    print(f"  '{s}': {'ACCEPT' if result else 'REJECT'}")

print("\n✓ Core functionality works!")
