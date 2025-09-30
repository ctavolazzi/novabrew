import pygame
from .tile import Tile
from ..utils.constants import *

class Room:
    def __init__(self, name, description, exits):
        self.name = name
        self.description = description
        self.exits = exits
        self.doors = []  # List to store door objects
        self.tile_size = TILE_SIZE
        self.width = WINDOW_WIDTH // self.tile_size
        self.height = WINDOW_HEIGHT // self.tile_size

        # Initialize empty tile grid
        self.grid = [[None for x in range(self.width)] for y in range(self.height)]

        # Fill room with floor tiles
        self.fill_floor()
        # Add walls around the edges
        self.add_walls()
        # Add doors based on exits
        self.add_doors()

        # Print the room layout
        self.print_room_layout()

    def fill_floor(self):
        """Fill the room with floor tiles"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = Tile('floor', x * self.tile_size, y * self.tile_size)

    def add_walls(self):
        """Add walls around the edges of the room"""
        print("Adding walls...")  # Debug print

        # Add top and bottom walls
        for x in range(self.width):
            self.grid[0][x] = Tile('wall', x * self.tile_size, 0)
            self.grid[self.height-1][x] = Tile('wall', x * self.tile_size, (self.height-1) * self.tile_size)
            print(f"Added wall at top ({x}, 0) and bottom ({x}, {self.height-1})")  # Debug print

        # Add left and right walls
        for y in range(self.height):
            self.grid[y][0] = Tile('wall', 0, y * self.tile_size)
            self.grid[y][self.width-1] = Tile('wall', (self.width-1) * self.tile_size, y * self.tile_size)
            print(f"Added wall at left (0, {y}) and right ({self.width-1}, {y})")  # Debug print

    def add_doors(self):
        """Add doors based on room exits"""
        middle_x = self.width // 2
        middle_y = self.height // 2

        if 'north' in self.exits:
            self.grid[0][middle_x] = Tile('door', middle_x * self.tile_size, 0)
        if 'south' in self.exits:
            self.grid[self.height-1][middle_x] = Tile('door', middle_x * self.tile_size, (self.height-1) * self.tile_size)
        if 'east' in self.exits:
            self.grid[middle_y][self.width-1] = Tile('door', (self.width-1) * self.tile_size, middle_y * self.tile_size)
        if 'west' in self.exits:
            self.grid[middle_y][0] = Tile('door', 0, middle_y * self.tile_size)

    def draw(self, screen):
        """Draw the room and all its elements"""
        # Debug print to verify method is being called
        print("Drawing room...")

        # Draw all tiles
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile:
                    print(f"Drawing tile at ({x}, {y}): {tile.type}")  # Debug print
                    tile.draw(screen)

    def is_walkable(self, x, y):
        """Check if a position is walkable"""
        # Convert pixel coordinates to grid coordinates
        grid_x = int(x // self.tile_size)
        grid_y = int(y // self.tile_size)

        # Check bounds
        if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            return False

        # Get tile at position
        tile = self.grid[grid_y][grid_x]
        return tile is None or (tile and tile.type != 'wall')

    def check_door_collisions(self, player_rect):
        """Check if player is colliding with any doors"""
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile and tile.type == 'door':
                    door_rect = pygame.Rect(tile.x, tile.y, self.tile_size, self.tile_size)
                    if player_rect.colliderect(door_rect):
                        # Determine door direction
                        if y == 0:
                            return self.exits.get('north'), 'north'
                        elif y == self.height - 1:
                            return self.exits.get('south'), 'south'
                        elif x == 0:
                            return self.exits.get('west'), 'west'
                        elif x == self.width - 1:
                            return self.exits.get('east'), 'east'
        return None, None

    def print_room_layout(self):
        """Print ASCII representation of room layout"""
        symbols = {
            'wall': '#',
            'floor': '.',
            'door': 'D',
            None: ' '
        }

        print(f"\nRoom Layout for {self.name}:")
        print("-" * (self.width + 2))
        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                tile = self.grid[y][x]
                tile_type = tile.type if tile else None
                row += symbols.get(tile_type, '?')
            row += "|"
            print(row)
        print("-" * (self.width + 2))