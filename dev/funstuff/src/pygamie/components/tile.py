import pygame

class Tile:
    def __init__(self, tile_type, x, y, size=32):
        self.type = tile_type
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)

        # Define tile properties based on type
        self.properties = {
            'floor': {
                'color': (100, 100, 50),
                'walkable': True,
                'transparent': True
            },
            'wall': {
                'color': (70, 70, 70),
                'walkable': False,
                'transparent': False
            },
            'door': {
                'color': (139, 69, 19),
                'walkable': True,
                'transparent': True
            }
        }.get(tile_type, {
            'color': (255, 0, 255),  # Purple for unknown types
            'walkable': False,
            'transparent': True
        })

    def draw(self, screen):
        """Draw the tile with debug coloring"""
        # Draw the main tile
        pygame.draw.rect(screen, self.properties['color'], self.rect)

        # Draw a more visible border based on tile type
        if self.type == 'wall':
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red border for walls
        elif self.type == 'door':
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)  # Blue border for doors
        else:
            pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)  # Default border

    @property
    def walkable(self):
        return self.properties['walkable']