import pygame
from .inventory import Inventory

class Player:
    def __init__(self, starting_room, game=None):
        self.current_room = starting_room
        self.game = game
        # Player position in room (center of screen)
        self.x = 400
        self.y = 300
        self.speed = 5
        self.size = 32

        # Create a simple player sprite (we can replace with actual sprite image later)
        self.sprite = pygame.Surface((self.size, self.size))
        self.sprite.fill((0, 255, 0))  # Green for now

        # Initialize inventory
        self.inventory = None  # Will be set when screen is available

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        if self.game:
            # Get current room
            current_room = self.game.rooms[self.current_room]

            # Check if new position is walkable
            if current_room.is_walkable(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def draw(self, screen):
        screen.blit(self.sprite, (self.x - self.size/2, self.y - self.size/2))

    def set_screen(self, screen):
        """Initialize inventory once screen is available"""
        self.inventory = Inventory(screen)

    def toggle_inventory(self):
        """Toggle inventory visibility"""
        if self.inventory:
            self.inventory.toggle_visibility()