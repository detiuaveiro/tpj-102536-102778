from enum import Enum
from typing import Optional

class FSM:
    
    def __init__(self, initial_state: Enum) -> None:
        self.current_state: Enum = initial_state
        self.mapping: dict[Enum, dict[Enum, tuple[Enum, callable]]] = {} # {event: {state: (next_state, callback)}}


    def get_state(self) -> Enum:
        return self.current_state
    

    def get_state_str(self) -> str:
        return self.current_state.value


    def set_transitions(self, *transitions: tuple[Enum, Enum, Enum, callable]) -> None:
        for event, current_state, next_state, callback in transitions:
            if event not in self.mapping:
                self.mapping[event] = {}
            self.mapping[event][current_state] = (next_state, callback)


    def update(self, event: Enum, **kwargs) -> None:
        transitions = self.mapping.get(event, None)
        if transitions is None or self.current_state not in transitions:
            return
        next_state, callback = transitions[self.current_state]
        self.current_state = next_state
        if callback is not None:
            callback(**kwargs)  