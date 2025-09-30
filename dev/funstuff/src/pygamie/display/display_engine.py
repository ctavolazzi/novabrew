import pygame
from ..utils.constants import *

class DisplayEngine:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.layers = {
            'background': [],
            'terrain': [],
            'items': [],
            'characters': [],
            'effects': [],
            'ui': []
        }

    def render(self, game):
        """Main render loop"""
        self.screen.fill((0, 0, 0))  # Clear screen

        # Get current room
        current_room = game.rooms[game.player.current_room]

        # Render room
        current_room.draw(self.screen)

        # Render player
        game.player.draw(self.screen)

        # Render UI elements
        game.map.render()
        game.hud.render()

        # Update display
        pygame.display.flip()