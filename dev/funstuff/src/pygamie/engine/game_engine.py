from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from ..utils.constants import *

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    INVENTORY = "inventory"
    DIALOG = "dialog"

class GameEngine:
    def __init__(self, game):
        self.game = game
        self.state = GameState.PLAYING
        self.event_handlers = {}

    def update(self, dt: float):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            self.game.handle_input()

    def register_handler(self, event_type: str, handler: callable):
        """Register event handlers"""
        self.event_handlers[event_type] = handler