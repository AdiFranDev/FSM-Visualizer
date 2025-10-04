"""Widget for automaton simulation."""

from ..qt_compat import QtWidgets, QtCore, Signal
from ..models.pda import PDA, PDAConfiguration
from ..models.mealy_moore import MealyMachine, MooreMachine
from ..visualization.simulator import SimulationResult

QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QLineEdit = QtWidgets.QLineEdit
QPushButton = QtWidgets.QPushButton
QTextEdit = QtWidgets.QTextEdit
QLabel = QtWidgets.QLabel


class SimulationWidget(QWidget):
    """Widget for step-by-step simulation."""
    
    simulate_requested = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Input string
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Input String:"))
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter input string...")
        self.input_field.returnPressed.connect(self.request_simulation)
        input_layout.addWidget(self.input_field)
        
        simulate_btn = QPushButton("Simulate")
        simulate_btn.clicked.connect(self.request_simulation)
        input_layout.addWidget(simulate_btn)
        
        layout.addLayout(input_layout)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMaximumHeight(200)
        layout.addWidget(self.results_display)
    
    def request_simulation(self):
        """Request simulation from main window."""
        input_string = self.input_field.text()
        self.simulate_requested.emit(input_string)
    
    def display_result(self, result: SimulationResult, automaton):
        """Display simulation result."""
        output = f"Input: '{self.input_field.text()}'\n"
        output += f"Result: {'ACCEPTED' if result.accepted else 'REJECTED'}\n"
        output += "\nSteps:\n"
        
        if isinstance(automaton, PDA):
            output += self._format_pda_steps(result.steps)
        elif isinstance(automaton, (MealyMachine, MooreMachine)):
            output += self._format_fsm_steps(result.steps, result.final_output)
        else:
            output += self._format_regular_steps(result.steps, automaton)
        
        self.results_display.setText(output)
    
    def _format_regular_steps(self, steps, automaton) -> str:
        """Format steps for DFA/NFA/ε-NFA."""
        from ..models.dfa import DFA
        output = ""
        
        for i, step in enumerate(steps):
            if isinstance(automaton, DFA):
                current, symbol, next_state = step
                output += f"{i+1}. ({current}, {symbol}) → {next_state}\n"
            else:  # NFA/ε-NFA
                current_states, symbol, next_states = step
                output += f"{i+1}. ({{{', '.join(sorted(current_states))}}}, {symbol}) → {{{', '.join(sorted(next_states))}}}\n"
        
        return output
    
    def _format_pda_steps(self, steps) -> str:
        """Format steps for PDA."""
        output = ""
        
        for i, (config, transition) in enumerate(steps):
            if i == 0:
                output += f"Initial: {config}\n"
            else:
                output += f"Step {i}: {transition}\n"
                output += f"  → {config}\n"
        
        return output
    
    def _format_fsm_steps(self, steps, outputs) -> str:
        """Format steps for Mealy/Moore machines."""
        output = ""
        
        if outputs:
            output += f"Output Sequence: {' '.join(outputs)}\n\n"
        
        for i, step in enumerate(steps):
            if len(step) == 4:
                current, symbol, out, next_state = step
                output += f"{i+1}. ({current}, {symbol}) → {next_state} / {out}\n"
            else:
                current, symbol, next_state = step[:3]
                output += f"{i+1}. ({current}, {symbol}) → {next_state}\n"
        
        return output
