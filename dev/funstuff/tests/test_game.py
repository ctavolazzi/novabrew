import pytest
import pygame
from pygamie.components.tile import Tile
from pygamie.components.room import Room
from pygamie.components.player import Player
from pygamie.utils.constants import *

# Initialize pygame for tests
pygame.init()
TEST_SCREEN = pygame.Surface((800, 600))

class TestTile:
    def test_tile_creation(self):
        tile = Tile('floor', 0, 0)
        assert tile.type == 'floor'
        assert tile.walkable == True

        wall = Tile('wall', 32, 32)
        assert wall.type == 'wall'
        assert wall.walkable == False

    def test_tile_properties(self):
        tile = Tile('floor', 0, 0)
        assert tile.rect.width == 32
        assert tile.rect.height == 32
        assert tile.properties['color'] == (100, 100, 50)

class TestRoom:
    def test_room_creation(self):
        room = Room('test_room', 'A test room', {'north': 'other_room'})
        assert room.name == 'test_room'
        assert 'north' in room.exits

    def test_room_tiles(self):
        room = Room('test_room', 'A test room', {})
        # Check if walls are created around edges
        assert room.get_tile(0, 0).type == 'wall'  # Top-left corner
        assert room.get_tile(room.width-1, 0).type == 'wall'  # Top-right corner
        # Check if floor tiles are created in middle
        assert room.get_tile(5, 5).type == 'floor'

    def test_room_walkable(self):
        room = Room('test_room', 'A test room', {})
        # Walls should not be walkable
        assert not room.is_walkable(0, 0)
        # Floor should be walkable
        assert room.is_walkable(160, 160)  # Middle of room

class TestPlayer:
    def test_player_creation(self):
        player = Player('start_room')
        assert player.current_room == 'start_room'
        assert player.x == 400  # Starting position
        assert player.y == 300

    def test_player_movement(self):
        player = Player('start_room')
        initial_x = player.x
        initial_y = player.y

        # Mock the game and room for movement testing
        class MockGame:
            def __init__(self):
                self.rooms = {'start_room': Room('start_room', 'test', {})}
        player.game = MockGame()

        # Test movement
        player.move(1, 0)  # Move right
        assert player.x > initial_x

        player.move(0, 1)  # Move down
        assert player.y > initial_y

def test_game_initialization():
    """Test basic game setup"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    assert pygame.get_init()
    assert screen.get_size() == (800, 600)

if __name__ == '__main__':
    pytest.main(['-v'])