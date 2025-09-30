import pygame

class Item:
    def __init__(self, name, description, icon_color=(200, 200, 200)):
        self.name = name
        self.description = description
        self.icon_color = icon_color
        # Create a simple colored square as the item icon (we can replace with sprites later)
        self.icon = pygame.Surface((32, 32))
        self.icon.fill(icon_color)
        pygame.draw.rect(self.icon, (255, 255, 255), self.icon.get_rect(), 2)

    def use(self, player):
        """Override this in subclasses for specific item behavior"""
        pass

    def get_description(self):
        return f"{self.name}: {self.description}"