"""Conversions between Mealy and Moore machines."""

from models.mealy_moore import MealyMachine, MooreMachine


def mealy_to_moore(mealy: MealyMachine) -> MooreMachine:
    """
    Convert a Mealy machine to a Moore machine.
    
    Args:
        mealy: The Mealy machine to convert
        
    Returns:
        Equivalent Moore machine
    """
    moore = MooreMachine()
    
    # Create states: for each (state, output) pair in Mealy
    # we need a corresponding state in Moore
    state_map = {}
    
    for state in mealy.states:
        # Find all possible outputs from this state
        outputs = set()
        for symbol in mealy.alphabet:
            if (state, symbol) in mealy.output_function:
                outputs.add(mealy.output_function[(state, symbol)])
        
        # Create Moore states for each output
        if not outputs:
            # No transitions from this state
            moore_state = f"{state}"
            moore.add_state(moore_state, output=None)
            state_map[(state, None)] = moore_state
        else:
            for output in outputs:
                moore_state = f"{state}_{output}"
                moore.add_state(moore_state, output=output)
                state_map[(state, output)] = moore_state
    
    # Set start state
    # Find output of first transition from start
    start_output = None
    for symbol in mealy.alphabet:
        if (mealy.start_state, symbol) in mealy.output_function:
            start_output = mealy.output_function[(mealy.start_state, symbol)]
            break
    
    moore.start_state = state_map[(mealy.start_state, start_output)]
    
    # Add transitions
    for (from_state, symbol), to_state in mealy.transitions.items():
        output = mealy.output_function.get((from_state, symbol))
        next_output = None
        
        # Find output of next state
        for next_symbol in mealy.alphabet:
            if (to_state, next_symbol) in mealy.output_function:
                next_output = mealy.output_function[(to_state, next_symbol)]
                break
        
        moore_from = state_map[(from_state, output)]
        moore_to = state_map[(to_state, next_output)]
        
        moore.add_transition(moore_from, moore_to, symbol)
    
    return moore


def moore_to_mealy(moore: MooreMachine) -> MealyMachine:
    """
    Convert a Moore machine to a Mealy machine.
    
    Args:
        moore: The Moore machine to convert
        
    Returns:
        Equivalent Mealy machine
    """
    mealy = MealyMachine()
    
    # Copy states
    for state in moore.states:
        mealy.add_state(state)
    
    # Set start state
    mealy.start_state = moore.start_state
    
    # Copy transitions and assign outputs based on destination state
    for (from_state, symbol), to_state in moore.transitions.items():
        mealy.add_transition(from_state, to_state, symbol)
        
        # Output is the output of the destination state in Moore
        output = moore.output_function.get(to_state)
        mealy.output_function[(from_state, symbol)] = output
    
    return mealy