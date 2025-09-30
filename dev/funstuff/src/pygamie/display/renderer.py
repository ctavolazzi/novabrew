import pygame
from ..utils.constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.layers = {
            'background': [],  # Background elements (floor, walls)
            'items': [],       # Items in the room
            'npcs': [],        # NPCs and enemies
            'player': [],      # Player character
            'effects': [],     # Visual effects (particles, etc)
            'ui': []          # UI elements (HUD, minimap, inventory)
        }

        # Visual settings
        self.lighting_enabled = True
        self.particle_effects = True
        self.color_scheme = {
            'floor': (100, 100, 50),
            'wall': (70, 70, 70),
            'door': (139, 69, 19),
            'player': GREEN,
            'ui_background': (30, 30, 30, 180)
        }

    def add_to_layer(self, layer_name, element):
        """Add an element to a specific render layer"""
        if layer_name in self.layers:
            self.layers[layer_name].append(element)

    def clear_layer(self, layer_name):
        """Clear all elements from a specific layer"""
        if layer_name in self.layers:
            self.layers[layer_name].clear()

    def render(self):
        """Render all layers in order"""
        self.screen.fill((20, 20, 20))  # Dark gray background

        # Render room (from background layer)
        if self.layers['background']:
            current_room = self.layers['background'][0]
            if hasattr(current_room, 'draw'):
                for y in range(current_room.height):
                    for x in range(current_room.width):
                        tile = current_room.grid[y][x]
                        if tile:
                            rect = pygame.Rect(
                                x * TILE_SIZE,
                                y * TILE_SIZE,
                                TILE_SIZE,
                                TILE_SIZE
                            )
                            if tile.type == 'wall':
                                pygame.draw.rect(self.screen, (255, 0, 0), rect)
                                pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)
                            elif tile.type == 'door':
                                pygame.draw.rect(self.screen, (0, 0, 255), rect)
                                pygame.draw.rect(self.screen, (0, 255, 255), rect, 2)
                            elif tile.type == 'floor':
                                pygame.draw.rect(self.screen, (0, 100, 0), rect)
                                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

        # Draw player
        if self.layers['player']:
            self.layers['player'][0].draw(self.screen)

        # Draw UI elements
        for element in self.layers['ui']:
            element.draw(self.screen)

        pygame.display.flip()

    def _render_background(self):
        """Render room background with improved visuals"""
        # Add subtle gradient to floor
        for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
            darkness = min(1.0, y / WINDOW_HEIGHT + 0.3)
            floor_color = tuple(int(c * darkness) for c in self.color_scheme['floor'])
            for x in range(0, WINDOW_WIDTH, TILE_SIZE):
                pygame.draw.rect(self.screen, floor_color,
                               (x, y, TILE_SIZE, TILE_SIZE))
                # Add subtle grid lines
                pygame.draw.rect(self.screen, GRAY,
                               (x, y, TILE_SIZE, TILE_SIZE), 1)

    def _apply_lighting(self):
        """Apply dynamic lighting effects"""
        # Create a surface for the lighting overlay
        light_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        light_surface.fill((0, 0, 0, 100))  # Dim ambient lighting

        # Add player light source (if player exists in layers)
        if self.layers['player']:
            player = self.layers['player'][0]
            light_pos = (player.x, player.y)
            pygame.draw.circle(light_surface, (0, 0, 0, 0), light_pos, 150)

        self.screen.blit(light_surface, (0, 0))

    def _render_particles(self):
        """Render particle effects"""
        # Add ambient particles, torch flames, etc.
        pass