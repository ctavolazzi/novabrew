import pygame
from pathlib import Path

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_resources(self, resource_path: Path):
        self.load_images(resource_path / "images")
        self.load_sounds(resource_path / "sounds")
        self.load_fonts(resource_path / "fonts")

    def load_images(self, image_path: Path):
        if image_path.exists():
            for image_file in image_path.glob("*.png"):
                name = image_file.stem
                self.images[name] = pygame.image.load(str(image_file))

    def load_sounds(self, sound_path: Path):
        if sound_path.exists():
            for sound_file in sound_path.glob("*.wav"):
                name = sound_file.stem
                self.sounds[name] = pygame.mixer.Sound(str(sound_file))

    def load_fonts(self, font_path: Path):
        if font_path.exists():
            for font_file in font_path.glob("*.ttf"):
                name = font_file.stem
                self.fonts[name] = str(font_file)