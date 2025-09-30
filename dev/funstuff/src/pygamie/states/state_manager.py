from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    INVENTORY = "inventory"
    DIALOG = "dialog"

class StateManager:
    def __init__(self):
        self.state_stack = []

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        if self.state_stack:
            return self.state_stack.pop()

    def get_current_state(self):
        return self.state_stack[-1] if self.state_stack else None

    def update(self):
        if current_state := self.get_current_state():
            # Update current state logic here
            pass