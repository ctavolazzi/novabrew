import pygame
from .utils.constants import *
from .components.player import Player
from .components.minimap import MiniMap
from .utils.level_loader import LevelLoader
from .levels.level1 import LEVEL_CONFIG
from .items.weapon import Weapon
from .items.potion import Potion
from .components.hud import HUD
from .display.renderer import Renderer
from .states.game_state import GameState
from .states.state_manager import StateManager
from .events.event_manager import EventManager
from .utils.resource_manager import ResourceManager
from .components.component_manager import ComponentManager
from .scenes.scene_manager import SceneManager
from pathlib import Path

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Zelda-style Adventure")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize core systems
        self.state_manager = StateManager()
        self.event_manager = EventManager()
        self.resource_manager = ResourceManager()
        self.component_manager = ComponentManager()
        self.scene_manager = SceneManager()
        self.renderer = Renderer(self.screen)

        # Load resources
        self.resource_manager.load_resources(Path("resources"))

        # Set up initial game state
        self.state_manager.push_state(GameState.MENU)

        # Load rooms from config
        self.rooms, starting_room = LevelLoader.load_level(LEVEL_CONFIG)
        print(f"Loaded rooms: {list(self.rooms.keys())}")

        # Initialize components
        self.player = Player(starting_room, self)
        self.player.set_screen(self.screen)
        self.map = MiniMap(self.screen, self.rooms)
        self.map.update_current_room(starting_room)  # Set initial room
        self.hud = HUD(self.screen)

        # Add elements to renderer layers
        self.renderer.add_to_layer('player', self.player)
        self.renderer.add_to_layer('ui', self.map)
        self.renderer.add_to_layer('ui', self.hud)

        # Create test items with specific types
        self.test_items = [
            Weapon("Rusty Sword", "A basic sword", damage=10),
            Weapon("Steel Dagger", "Quick but weak", damage=5),
            Potion("Health Potion", "Restores 20 HP", heal_amount=20)
        ]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        if dx != 0 or dy != 0:
            self.player.move(dx, dy)

            # Check for door collisions after movement
            current_room = self.rooms[self.player.current_room]
            player_rect = pygame.Rect(self.player.x - self.player.size/2,
                                    self.player.y - self.player.size/2,
                                    self.player.size, self.player.size)

            next_room, direction = current_room.check_door_collisions(player_rect)
            if next_room:
                self.player.current_room = next_room
                # Update minimap with new room
                self.map.update_current_room(next_room)
                # Position player at opposite door in new room
                if direction == 'north':
                    self.player.y = WINDOW_HEIGHT - 100
                elif direction == 'south':
                    self.player.y = 100
                elif direction == 'east':
                    self.player.x = 100
                elif direction == 'west':
                    self.player.x = WINDOW_WIDTH - 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:  # 'I' key toggles inventory
                    self.player.toggle_inventory()

    def update(self):
        self.state_manager.update()
        self.component_manager.update()
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.update()

    def render(self):
        """Render the current game state"""
        # Clear all layers
        for layer_name in self.renderer.layers:
            self.renderer.clear_layer(layer_name)

        # Add current room to background layer
        current_room = self.rooms[self.player.current_room]
        self.renderer.add_to_layer('background', current_room)

        # Add player to player layer
        self.renderer.add_to_layer('player', self.player)

        # Add UI elements
        self.renderer.add_to_layer('ui', self.map)
        self.renderer.add_to_layer('ui', self.hud)

        # Render everything
        self.renderer.render()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
