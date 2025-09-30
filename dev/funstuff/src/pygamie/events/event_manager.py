from typing import Callable, Dict, List
from enum import Enum

class GameEvent(Enum):
    PLAYER_MOVE = "player_move"
    ROOM_CHANGE = "room_change"
    INVENTORY_TOGGLE = "inventory_toggle"
    ITEM_PICKUP = "item_pickup"

class EventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def dispatch(self, event_type, data=None):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)