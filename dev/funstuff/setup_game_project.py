import os
import shutil
import sys

def ask_yes_no(question):
    """Ask a yes/no question and return True/False."""
    while True:
        response = input(f"{question} (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please answer 'y' or 'n'")

def check_existing_files(dirs, files):
    """Check for existing directories and files."""
    existing = []

    # Check directories
    for d in dirs:
        if os.path.exists(d):
            existing.append(f"Directory: {d}")

    # Check specific files
    for f in files:
        if os.path.exists(f):
            existing.append(f"File: {f}")

    return existing

def create_file(path, content=''):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def setup_project():
    print("🎮 Setting up PyGame project structure...")

    # Base directories to create
    dirs = [
        'src/pygamie',
        'src/pygamie/assets/images',
        'src/pygamie/assets/sounds',
        'src/pygamie/assets/fonts',
        'src/pygamie/components',
        'src/pygamie/utils',
        'src/pygamie/levels',
        'src/pygamie/states',
        'tests'
    ]

    # Key files that will be created
    files = [
        'pyproject.toml',
        'src/pygamie/game.py',
        'src/pygamie/utils/constants.py',
        'src/pygamie/states/menu.py',
        'src/pygamie/components/player.py',
        'src/pygamie/states/playing.py',
        'tests/test_player.py'
    ]

    # Check for existing content
    existing = check_existing_files(dirs, files)

    if existing:
        print("\n⚠️  Warning: The following already exist:")
        for item in existing:
            print(f"  - {item}")

        if not ask_yes_no("\n❓ Do you want to overwrite existing files/directories?"):
            print("\n🛑 Setup cancelled. No changes were made.")
            return False

        print("\n🗑️  Cleaning existing directories...")
        for d in dirs:
            if os.path.exists(d):
                shutil.rmtree(d)

    print("\n📁 Creating project structure...")

    try:
        # First, clean up redundant directories
        redundant_dirs = [
            'src/assets',
            'src/components',
            'src/levels',
            'src/states',
            'src/utils'
        ]

        print("\n🧹 Cleaning up redundant directories...")
        for d in redundant_dirs:
            if os.path.exists(d):
                shutil.rmtree(d)

        # Create directories
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            if 'assets' not in d:
                create_file(os.path.join(d, '__init__.py'))

        # Create game.py with a moving rectangle
        create_file('src/pygamie/game.py', '''import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PyGame Project")
clock = pygame.time.Clock()

# Player rectangle
player_rect = pygame.Rect(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 50, 50)
player_speed = 5

def main():
    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # Keep player on screen
        player_rect.clamp_ip(screen.get_rect())

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, player_rect)
        pygame.display.flip()

        # Control game speed
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
''')

        # Create constants.py
        create_file('src/pygamie/utils/constants.py', '''# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
''')

        print("\n✅ Project structure created successfully!")
        print("\n📝 To run the game:")
        print("1. poetry install")
        print("2. poetry run python src/pygamie/game.py")

        return True

    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        if setup_project():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelled by user.")
        sys.exit(1)