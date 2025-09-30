import pygame
from ..utils.constants import *

class MiniMap:
    def __init__(self, screen, rooms):
        self.screen = screen
        self.rooms = rooms
        self.room_size = 40
        self.current_room = next(iter(rooms.keys()))  # Default to first room
        self.padding = 10

    def update_current_room(self, room_id):
        """Update the current room marker"""
        self.current_room = room_id

    def draw(self, screen):
        """Draw method for renderer compatibility"""
        # Calculate room positions
        room_positions = self._calculate_room_positions()

        # Draw the minimap in the top-right corner
        minimap_surface = pygame.Surface((200, 200))
        minimap_surface.fill((0, 0, 0))
        minimap_surface.set_alpha(180)

        # Draw connections between rooms
        self._draw_connections(room_positions)

        # Draw rooms
        self._draw_rooms(room_positions, self.current_room)

        # Position minimap in top-right corner
        screen.blit(minimap_surface, (WINDOW_WIDTH - 220, 20))

    def _calculate_room_positions(self):
        """Calculate room positions based on their exits/connections"""
        positions = {}
        grid = {}  # Track room positions in a 2D grid
        visited = set()

        # Start with first room at (0,0) in our grid
        start_room = next(iter(self.rooms))
        grid[(0,0)] = start_room
        positions[start_room] = (WINDOW_WIDTH - 220 + 100, 20 + 100)

        def place_connected_rooms(room_id, grid_x, grid_y):
            if room_id in visited:
                return
            visited.add(room_id)
            room = self.rooms[room_id]

            # Define grid offsets for each direction
            directions = {
                'north': (0, -1),
                'south': (0, 1),
                'east': (1, 0),
                'west': (-1, 0)
            }

            # Place connected rooms in grid
            for exit_dir, target_room in room.exits.items():
                if target_room not in visited:
                    dx, dy = directions[exit_dir]
                    new_x, new_y = grid_x + dx, grid_y + dy
                    if (new_x, new_y) not in grid:
                        grid[(new_x, new_y)] = target_room
                        # Convert grid position to screen coordinates
                        screen_x = WINDOW_WIDTH - 220 + 100 + (new_x * 40)
                        screen_y = 20 + 100 + (new_y * 40)
                        positions[target_room] = (screen_x, screen_y)
                        place_connected_rooms(target_room, new_x, new_y)

        # Start placement from first room
        place_connected_rooms(start_room, 0, 0)
        return positions

    def _draw_connections(self, room_positions):
        """Draw lines between connected rooms"""
        for room_id, room in self.rooms.items():
            if room_id in room_positions:
                start_pos = room_positions[room_id]
                for exit_dir, target_room in room.exits.items():
                    if target_room in room_positions:
                        end_pos = room_positions[target_room]
                        pygame.draw.line(self.screen, (100, 100, 100),
                                       start_pos, end_pos, 2)

    def _draw_rooms(self, room_positions, current_room):
        """Draw each room as a rectangle with its name"""
        for room_id, pos in room_positions.items():
            # Draw room rectangle
            color = (200, 50, 50) if room_id == current_room else (70, 70, 70)
            room_rect = pygame.Rect(pos[0] - self.room_size//2,
                                  pos[1] - self.room_size//2,
                                  self.room_size, self.room_size)
            pygame.draw.rect(self.screen, color, room_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), room_rect, 2)

            # Draw room name
            font = pygame.font.Font(None, 24)
            text = font.render(room_id.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=pos)
            self.screen.blit(text, text_rect)