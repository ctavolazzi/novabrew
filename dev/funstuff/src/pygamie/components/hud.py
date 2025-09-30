import pygame
from ..utils.constants import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.padding = 10
        self.controls = [
            ("WASD/Arrows", "Move"),
            ("I", "Toggle Inventory"),
            ("ESC", "Quit Game"),
            # Add more controls here as we add features
        ]

    def draw(self, screen):
        """Draw method for renderer compatibility"""
        # Draw semi-transparent background for controls
        help_surface = pygame.Surface((200, len(self.controls) * 25 + 20))
        help_surface.fill((0, 0, 0))
        help_surface.set_alpha(128)
        screen.blit(help_surface, (10, 10))

        # Draw controls list
        y = 20
        for key, action in self.controls:
            # Draw key binding
            key_text = self.font.render(key, True, (255, 255, 255))
            screen.blit(key_text, (20, y))

            # Draw action description
            action_text = self.font.render(action, True, (200, 200, 200))
            screen.blit(action_text, (100, y))

            y += 25