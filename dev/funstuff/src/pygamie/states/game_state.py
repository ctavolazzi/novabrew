from enum import Enum, auto
from typing import Dict, Optional, Callable

class GameState(Enum):
    # Core game states
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()

    # Overlay states (can be active during PLAYING)
    INVENTORY = auto()
    DIALOG = auto()

    # End states
    GAME_OVER = auto()
    VICTORY = auto()

class StateManager:
    def __init__(self):
        self.state_stack = []
        self.state_handlers: Dict[GameState, Callable] = {}
        self.valid_transitions: Dict[GameState, list[GameState]] = {
            GameState.MENU: [GameState.PLAYING],
            GameState.PLAYING: [GameState.PAUSED, GameState.INVENTORY, GameState.DIALOG, GameState.GAME_OVER],
            GameState.PAUSED: [GameState.PLAYING, GameState.MENU],
            GameState.INVENTORY: [GameState.PLAYING],
            GameState.DIALOG: [GameState.PLAYING],
            GameState.GAME_OVER: [GameState.MENU],
            GameState.VICTORY: [GameState.MENU]
        }

    def get_current_state(self) -> Optional[GameState]:
        """Return the current state, or None if no state is active"""
        return self.state_stack[-1] if self.state_stack else None

    def can_transition_to(self, new_state: GameState) -> bool:
        """Check if transition to new_state is valid from current state"""
        current = self.get_current_state()
        return current is None or new_state in self.valid_transitions[current]

    def push_state(self, new_state: GameState) -> bool:
        """Push a new state if transition is valid"""
        if self.can_transition_to(new_state):
            self.state_stack.append(new_state)
            return True
        return False

    def pop_state(self) -> Optional[GameState]:
        """Remove and return the top state if there is one"""
        return self.state_stack.pop() if self.state_stack else None

    def register_handler(self, state: GameState, handler: Callable):
        """Register a handler function for a state"""
        self.state_handlers[state] = handler

    def update(self):
        """Update current state"""
        if current := self.get_current_state():
            if handler := self.state_handlers.get(current):
                handler()