import pygame
from ..utils.constants import *

class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.items = []
        self.capacity = 12  # 3x4 grid
        self.selected_slot = 0
        self.visible = False
        self.slot_size = 40
        self.padding = 10

        # Calculate inventory window size
        self.cols = 4
        self.rows = 3
        self.width = (self.slot_size * self.cols) + (self.padding * (self.cols + 1))
        self.height = (self.slot_size * self.rows) + (self.padding * (self.rows + 1))

        # Center the inventory on screen
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = (WINDOW_HEIGHT - self.height) // 2

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def get_selected_item(self):
        if 0 <= self.selected_slot < len(self.items):
            return self.items[self.selected_slot]
        return None

    def toggle_visibility(self):
        self.visible = not self.visible

    def render(self):
        if not self.visible:
            return

        # Draw inventory background
        inventory_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, (50, 50, 50), inventory_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), inventory_rect, 2)

        # Draw slots and items
        for i in range(self.capacity):
            row = i // self.cols
            col = i % self.cols

            # Calculate slot position
            slot_x = self.x + self.padding + (col * (self.slot_size + self.padding))
            slot_y = self.y + self.padding + (row * (self.slot_size + self.padding))

            # Draw slot
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            pygame.draw.rect(self.screen, (70, 70, 70), slot_rect)

            # Highlight selected slot
            if i == self.selected_slot:
                pygame.draw.rect(self.screen, (255, 255, 255), slot_rect, 2)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), slot_rect, 1)

            # Draw item if slot is filled
            if i < len(self.items):
                item = self.items[i]
                item_rect = item.icon.get_rect(center=slot_rect.center)
                self.screen.blit(item.icon, item_rect)