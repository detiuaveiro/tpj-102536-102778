from enum import Enum

class FSM:
    """
    Finite State Machine class.
    """
    
    def __init__(self, initial_state: Enum) -> None:
        """
        Parameters
        ----------
        initial_state (Enum):
            Initial state of the machine.

        Attributes
        ----------
        current_state (Enum):
            Current state of the machine.
        mapping (dict[Enum, dict[Enum, tuple[Enum, callable]]]):
            Mapping of events to states and their transitions.
        """
        self.current_state: Enum = initial_state
        self.mapping: dict[Enum, dict[Enum, tuple[Enum, callable]]] = {} # {event: {state: (next_state, callback)}}


    def get_state(self) -> Enum:
        """
        Returns
        -------
        Enum:
            Current state of the machine.
        """
        return self.current_state
    

    def get_state_str(self) -> str:
        """
        Returns
        -------
        str:
            Current state of the machine as a string.
        """
        return self.current_state.value


    def set_transitions(self, *transitions: tuple[Enum, Enum, Enum, callable]) -> None:
        """
        Set transitions for the machine.

        Parameters
        ----------
        transitions (tuple[Enum, Enum, Enum, callable]):
            Transitions to be set for the machine.
            Each transition is a tuple with the following elements:
                - event (Enum): Event that triggers the transition.
                - current_state (Enum): Current state of the machine.
                - next_state (Enum): Next state of the machine.
                - callback (callable): Callback function to be called when the transition is triggered.
        """
        for event, current_state, next_state, callback in transitions:
            if event not in self.mapping:
                self.mapping[event] = {}
            self.mapping[event][current_state] = (next_state, callback)


    def update(self, event: Enum, **kwargs) -> None:
        """
        Update the machine based on an event.

        Parameters
        ----------
        event (Enum):
            Event that triggers the update.
        kwargs (dict):
            Arguments for the event that are passed to the callback function.
        """
        transitions = self.mapping.get(event, None)
        if transitions is None or self.current_state not in transitions:
            return
        next_state, callback = transitions[self.current_state]
        self.current_state = next_state
        if callback is not None:
            callback(**kwargs)  