"""Main window for the FSM Visualizer application."""

from ..qt_compat import QtWidgets, QtCore, QtGui
import tempfile
import os
import subprocess

from ..parsers.json_parser import parse_json_automaton
from ..parsers.text_parser import parse_text_automaton
from ..algorithms.thompson import thompson_construction
from ..algorithms.subset_construction import epsilon_nfa_to_nfa, nfa_to_dfa
from ..algorithms.minimization import minimize_dfa
from ..algorithms.conversions import mealy_to_moore, moore_to_mealy
from ..visualization.graph_renderer import render_automaton, export_graph
from ..visualization.simulator import simulate_automaton
from ..models.dfa import DFA
from ..models.mealy_moore import MealyMachine, MooreMachine
from .input_dialog import InputDialog
from .simulation_widget import SimulationWidget
from .export_dialog import ExportDialog


class MainWindow(QtWidgets.QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.current_automaton = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("FSM Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menus()
        
        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        
        # Left panel: Input and controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Visualization
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_menus(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Try to get QAction from correct module
        try:
            QAction = QtGui.QAction
        except AttributeError:
            QAction = QtWidgets.QAction
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save As...", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export Graph...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_graph_dialog)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Convert menu
        convert_menu = menubar.addMenu("&Convert")
        
        regex_action = QAction("Regex to ε-NFA", self)
        regex_action.triggered.connect(self.convert_regex_to_enfa)
        convert_menu.addAction(regex_action)
        
        enfa_nfa_action = QAction("ε-NFA to NFA", self)
        enfa_nfa_action.triggered.connect(self.convert_enfa_to_nfa)
        convert_menu.addAction(enfa_nfa_action)
        
        nfa_dfa_action = QAction("NFA to DFA", self)
        nfa_dfa_action.triggered.connect(self.convert_nfa_to_dfa)
        convert_menu.addAction(nfa_dfa_action)
        
        minimize_action = QAction("Minimize DFA", self)
        minimize_action.triggered.connect(self.minimize_dfa_action)
        convert_menu.addAction(minimize_action)
        
        convert_menu.addSeparator()
        
        mealy_moore_action = QAction("Mealy to Moore", self)
        mealy_moore_action.triggered.connect(self.convert_mealy_to_moore)
        convert_menu.addAction(mealy_moore_action)
        
        moore_mealy_action = QAction("Moore to Mealy", self)
        moore_mealy_action.triggered.connect(self.convert_moore_to_mealy)
        convert_menu.addAction(moore_mealy_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_left_panel(self) -> QtWidgets.QWidget:
        """Create left panel with input controls."""
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        
        # Input tabs
        self.input_tabs = QtWidgets.QTabWidget()
        
        # JSON input tab
        json_widget = QtWidgets.QWidget()
        json_layout = QtWidgets.QVBoxLayout(json_widget)
        self.json_input = QtWidgets.QTextEdit()
        self.json_input.setPlaceholderText("Enter JSON automaton definition...")
        json_layout.addWidget(self.json_input)
        self.input_tabs.addTab(json_widget, "JSON")
        
        # Text input tab
        text_widget = QtWidgets.QWidget()
        text_layout = QtWidgets.QVBoxLayout(text_widget)
        self.text_input = QtWidgets.QTextEdit()
        self.text_input.setPlaceholderText("Enter text automaton definition...")
        text_layout.addWidget(self.text_input)
        self.input_tabs.addTab(text_widget, "Text")
        
        # Regex input tab
        regex_widget = QtWidgets.QWidget()
        regex_layout = QtWidgets.QVBoxLayout(regex_widget)
        self.regex_input = QtWidgets.QTextEdit()
        self.regex_input.setPlaceholderText("Enter regular expression...\nExample: (a|b)*abb")
        regex_layout.addWidget(self.regex_input)
        self.input_tabs.addTab(regex_widget, "Regex")
        
        layout.addWidget(self.input_tabs)
        
        # Parse button
        parse_btn = QtWidgets.QPushButton("Parse & Visualize")
        parse_btn.clicked.connect(self.parse_and_visualize)
        layout.addWidget(parse_btn)
        
        # Simulation section
        layout.addWidget(QtWidgets.QLabel("Simulation:"))
        
        self.simulation_widget = SimulationWidget()
        self.simulation_widget.simulate_requested.connect(self.run_simulation)
        layout.addWidget(self.simulation_widget)
        
        return panel
    
    def create_right_panel(self) -> QtWidgets.QWidget:
        """Create right panel for visualization."""
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        
        # Graph display
        self.graph_label = QtWidgets.QLabel("No automaton loaded")
        self.graph_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.graph_label.setStyleSheet("border: 1px solid #ccc; background: white;")
        self.graph_label.setMinimumSize(400, 400)
        layout.addWidget(self.graph_label)
        
        # Info display
        self.info_text = QtWidgets.QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(150)
        layout.addWidget(self.info_text)
        
        return panel
    
    def parse_and_visualize(self):
        """Parse input and visualize the automaton."""
        current_tab = self.input_tabs.currentIndex()
        
        try:
            if current_tab == 0:  # JSON
                json_text = self.json_input.toPlainText().strip()
                if not json_text:
                    raise ValueError("JSON input is empty")
                self.current_automaton = parse_json_automaton(json_text)
            
            elif current_tab == 1:  # Text
                text = self.text_input.toPlainText().strip()
                if not text:
                    raise ValueError("Text input is empty")
                self.current_automaton = parse_text_automaton(text)
            
            elif current_tab == 2:  # Regex
                regex = self.regex_input.toPlainText().strip()
                if not regex:
                    raise ValueError("Regex input is empty")
                self.current_automaton = thompson_construction(regex)
            
            # Validate
            is_valid, msg = self.current_automaton.validate()
            if not is_valid:
                raise ValueError(f"Invalid automaton: {msg}")
            
            # Visualize
            self.visualize_current_automaton()
            self.statusBar().showMessage("Automaton loaded successfully")
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to parse automaton:\n{str(e)}")
            self.statusBar().showMessage("Error parsing automaton")
    
    def visualize_current_automaton(self):
        """Visualize the current automaton."""
        if self.current_automaton is None:
            return
        
        try:
            # Check if Graphviz is available
            try:
                subprocess.run(['dot', '-V'], capture_output=True, timeout=5, check=True)
            except (FileNotFoundError, subprocess.SubprocessError):
                error_msg = (
                    "Graphviz is not installed or not in your system PATH.\n\n"
                    "Please install Graphviz:\n"
                    "• Windows: Download from https://graphviz.org/download/\n"
                    "            or run: choco install graphviz\n"
                    "• macOS: brew install graphviz\n"
                    "• Linux: sudo apt-get install graphviz\n\n"
                    "After installation, restart your terminal/IDE and try again."
                )
                QtWidgets.QMessageBox.critical(self, "Graphviz Not Found", error_msg)
                return
            
            # Render graph
            dot = render_automaton(self.current_automaton)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                tmp_path = tmp.name
            
            dot.render(tmp_path.replace('.png', ''), format='png', cleanup=True)
            
            # Display image
            pixmap = QtGui.QPixmap(tmp_path)
            scaled_pixmap = pixmap.scaled(self.graph_label.size(), 
                                         QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                         QtCore.Qt.TransformationMode.SmoothTransformation)
            self.graph_label.setPixmap(scaled_pixmap)
            
            # Clean up
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            # Update info
            self.update_info_display()
        
        except Exception as e:
            error_msg = f"Failed to visualize automaton:\n{str(e)}\n\n"
            if "dot" in str(e).lower() or "graphviz" in str(e).lower():
                error_msg += (
                    "This appears to be a Graphviz issue.\n"
                    "Make sure Graphviz is installed and in your PATH."
                )
            QtWidgets.QMessageBox.critical(self, "Visualization Error", error_msg)
    
    def update_info_display(self):
        """Update the information display."""
        if self.current_automaton is None:
            return
        
        info = f"Type: {type(self.current_automaton).__name__}\n"
        info += f"States: {self.current_automaton.get_state_count()}\n"
        info += f"Transitions: {self.current_automaton.get_transition_count()}\n"
        info += f"Alphabet: {{{', '.join(sorted(self.current_automaton.alphabet))}}}\n"
        info += f"Start State: {self.current_automaton.start_state}\n"
        info += f"Accept States: {{{', '.join(sorted(self.current_automaton.accept_states))}}}\n"
        
        self.info_text.setText(info)
    
    def run_simulation(self, input_string: str):
        """Run simulation on input string."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        try:
            result = simulate_automaton(self.current_automaton, input_string)
            self.simulation_widget.display_result(result, self.current_automaton)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Simulation Error", 
                               f"Failed to simulate:\n{str(e)}")
    
    # Conversion methods
    def convert_regex_to_enfa(self):
        """Convert regex to ε-NFA."""
        dialog = InputDialog("Enter Regular Expression", "Regex:", self)
        if dialog.exec():
            regex = dialog.get_input()
            try:
                self.current_automaton = thompson_construction(regex)
                self.visualize_current_automaton()
                self.statusBar().showMessage("Converted regex to ε-NFA")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Conversion failed:\n{str(e)}")
    
    def convert_enfa_to_nfa(self):
        """Convert ε-NFA to NFA."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        try:
            from ..models.nfa import EpsilonNFA
            if not isinstance(self.current_automaton, EpsilonNFA):
                raise ValueError("Current automaton is not an ε-NFA")
            
            self.current_automaton = epsilon_nfa_to_nfa(self.current_automaton)
            self.visualize_current_automaton()
            self.statusBar().showMessage("Converted ε-NFA to NFA")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Conversion failed:\n{str(e)}")
    
    def convert_nfa_to_dfa(self):
        """Convert NFA to DFA."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        try:
            from ..models.nfa import NFA
            if not isinstance(self.current_automaton, NFA):
                raise ValueError("Current automaton is not an NFA")
            
            self.current_automaton = nfa_to_dfa(self.current_automaton)
            self.visualize_current_automaton()
            self.statusBar().showMessage("Converted NFA to DFA")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Conversion failed:\n{str(e)}")
    
    def minimize_dfa_action(self):
        """Minimize current DFA."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        try:
            if not isinstance(self.current_automaton, DFA):
                raise ValueError("Current automaton is not a DFA")
            
            self.current_automaton = minimize_dfa(self.current_automaton)
            self.visualize_current_automaton()
            self.statusBar().showMessage("DFA minimized")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Minimization failed:\n{str(e)}")
    
    def convert_mealy_to_moore(self):
        """Convert Mealy to Moore."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        try:
            if not isinstance(self.current_automaton, MealyMachine):
                raise ValueError("Current automaton is not a Mealy machine")
            
            self.current_automaton = mealy_to_moore(self.current_automaton)
            self.visualize_current_automaton()
            self.statusBar().showMessage("Converted Mealy to Moore")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Conversion failed:\n{str(e)}")
    
    def convert_moore_to_mealy(self):
        """Convert Moore to Mealy."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        try:
            if not isinstance(self.current_automaton, MooreMachine):
                raise ValueError("Current automaton is not a Moore machine")
            
            self.current_automaton = moore_to_mealy(self.current_automaton)
            self.visualize_current_automaton()
            self.statusBar().showMessage("Converted Moore to Mealy")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Conversion failed:\n{str(e)}")
    
    def open_file(self):
        """Open file dialog."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Automaton File", "", 
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                
                if filename.endswith('.json'):
                    self.json_input.setText(content)
                    self.input_tabs.setCurrentIndex(0)
                else:
                    self.text_input.setText(content)
                    self.input_tabs.setCurrentIndex(1)
                
                self.parse_and_visualize()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")
    
    def save_file(self):
        """Save current input to file."""
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Automaton", "",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                current_tab = self.input_tabs.currentIndex()
                if current_tab == 0:
                    content = self.json_input.toPlainText()
                elif current_tab == 1:
                    content = self.text_input.toPlainText()
                else:
                    content = self.regex_input.toPlainText()
                
                with open(filename, 'w') as f:
                    f.write(content)
                
                self.statusBar().showMessage(f"Saved to {filename}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def export_graph_dialog(self):
        """Show export dialog."""
        if self.current_automaton is None:
            QtWidgets.QMessageBox.warning(self, "No Automaton", "Please load an automaton first")
            return
        
        dialog = ExportDialog(self)
        if dialog.exec():
            filepath, format_type = dialog.get_export_info()
            try:
                export_graph(self.current_automaton, filepath, format_type)
                QtWidgets.QMessageBox.information(self, "Success", 
                                      f"Graph exported to {filepath}.{format_type}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        QtWidgets.QMessageBox.about(self, "About FSM Visualizer",
                         "FSM Visualizer v1.0\n\n"
                         "A tool for visualizing and simulating:\n"
                         "• DFA, NFA, ε-NFA\n"
                         "• PDA\n"
                         "• Mealy and Moore machines\n\n"
     "Built with PyQt6/PySide6 and Graphviz")
