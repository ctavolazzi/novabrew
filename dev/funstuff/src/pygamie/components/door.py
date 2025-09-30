import pygame
from ..utils.constants import *

class Door:
    def __init__(self, x, y, width, height, target_room, direction):
        self.rect = pygame.Rect(x, y, width, height)
        self.target_room = target_room
        self.direction = direction
        self.color = (139, 69, 19)  # Brown door color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw door frame
        pygame.draw.rect(screen, (101, 67, 33), self.rect, 3)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)