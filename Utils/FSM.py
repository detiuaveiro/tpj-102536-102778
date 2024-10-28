from enum import Enum
from typing import Optional

class FSM:
    
    def __init__(self):
        self.current_state: Optional[Enum] = None
        self.mapping: dict[str, dict[Enum, tuple[Enum, callable]]] = {} # {key: {state: (next_state, callback)}}


    def set_state(self, state: Enum) -> None:
        self.current_state = state


    def set_transitions(self, *transitions: tuple[str, Enum, Enum, callable]) -> None:
        for key, current_state, next_state, callback in transitions:
            if key not in self.mapping:
                self.mapping[key] = {}
            self.mapping[key][current_state] = (next_state, callback)


    def change_key(self, old: str, new: str) -> None:
        self.mapping[new] = self.mapping.pop(old)


    def update(self, key: str, **kwargs) -> None:
        transitions = self.mapping.get(key, None)
        if transitions is None or self.current_state not in transitions:
            return
        next_state, callback = transitions[self.current_state]
        self.current_state = next_state
        if callback is not None:
            callback(**kwargs)  