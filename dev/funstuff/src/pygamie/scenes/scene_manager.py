class Scene:
    def __init__(self):
        self.entities = []

    def update(self):
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update()

    def render(self, renderer):
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(renderer)

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]