# FSM Visualizer

A desktop application for visualizing and simulating finite automata, pushdown automata, and finite state machines.

## Features

- **Automata Types**: DFA, NFA, ε-NFA, PDA, Mealy, and Moore machines
- **Conversions**: Regular expression → ε-NFA → NFA → DFA → Minimal DFA
- **Mealy ↔ Moore**: Bidirectional conversion between Mealy and Moore machines
- **Visualization**: Clear graph rendering using Graphviz
- **Simulation**: Step-by-step execution with stack visualization for PDA
- **Export**: Save graphs as PNG or SVG

## Requirements

- Python 3.10 or later
- Graphviz system binary (not just the Python package)

## Installation

### Step 1: Install Graphviz System Binary (REQUIRED)

**This is a system-level dependency, not just a Python package!**

#### Windows

**Option A: Using Installer (Recommended)**
1. Download from https://graphviz.org/download/
2. Run the installer
3. **IMPORTANT**: During installation, check "Add Graphviz to the system PATH"
4. Restart your terminal/IDE

**Option B: Using Chocolatey**
```bash
choco install graphviz
```

#### macOS
```bash
brew install graphviz
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install graphviz
```

### Step 2: Verify Graphviz Installation

```bash
python check_graphviz.py
```

This should show:

```
Graphviz is installed and working!
```

If you see an error, Graphviz is not installed correctly. Please reinstall it.

### Step 3: Install Python Dependencies

```bash
cd "c:\Users\Adrian\OneDrive\Desktop\Projects\Python Projects\School\FSM Visualizer"
pip install -r requirements.txt
```

### Troubleshooting Installation Issues

**PyQt6 DLL Error on Windows:**

If you get "DLL load failed" error when importing PyQt6:

```bash
# Try reinstalling with specific versions
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
pip install PyQt6==6.6.1 PyQt6-Qt6==6.6.1 PyQt6-sip==13.6.0
```

If that doesn't work, try an older version:

```bash
pip install PyQt6==6.5.0
```

Or use the dependency checker:

```bash
python launch.py
```

**Alternative: Use PySide6**

If PyQt6 continues to have issues, you can use PySide6 instead (API is nearly identical):

```bash
pip uninstall PyQt6 -y
pip install PySide6
```

Then in the code, replace all `PyQt6` imports with `PySide6`.

## Running the Application

```bash
python src/main.py
```

Or use the launcher with dependency checking:

```bash
python launch.py
```

## Input Formats

### JSON Format

**DFA/NFA Example:**
```json
{
  "type": "dfa",
  "states": ["q0", "q1", "q2"],
  "alphabet": ["0", "1"],
  "start_state": "q0",
  "accept_states": ["q2"],
  "transitions": {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q2", "1": "q0"},
    "q2": {"0": "q2", "1": "q2"}
  }
}
```

**PDA Example:**
```json
{
  "type": "pda",
  "states": ["q0", "q1", "q2"],
  "input_alphabet": ["0", "1"],
  "stack_alphabet": ["Z", "X"],
  "start_state": "q0",
  "start_stack": "Z",
  "accept_states": ["q2"],
  "transitions": {
    "q0": [
      {"input": "0", "stack_pop": "Z", "next_state": "q0", "stack_push": ["X", "Z"]}
    ]
  }
}
```

**Mealy Machine Example:**
```json
{
  "type": "mealy",
  "states": ["A", "B"],
  "input_alphabet": ["0", "1"],
  "output_alphabet": ["x", "y"],
  "start_state": "A",
  "transitions": {
    "A": {"0": {"next_state": "B", "output": "x"}},
    "B": {"1": {"next_state": "A", "output": "y"}}
  }
}
```

### Regular Expression Format

Simply enter a regular expression string:
- `a*b+`
- `(a|b)*abb`
- `(0|1)*00(0|1)*`

Supported operators: `*` (star), `+` (plus), `|` (or), `()` (grouping), `ε` (epsilon)

## Running Tests

```bash
pytest tests/
```

## Examples

Check the `examples/` folder for sample input files.

## License

MIT License
