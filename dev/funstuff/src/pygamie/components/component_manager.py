from typing import Dict, Any

class Component:
    def __init__(self):
        self.entity = None

    def update(self):
        pass

class Entity:
    def __init__(self):
        self.components: Dict[str, Component] = {}

    def add_component(self, component_type: str, component: Component):
        component.entity = self
        self.components[component_type] = component

    def get_component(self, component_type: str) -> Component:
        return self.components.get(component_type)

class ComponentManager:
    def __init__(self):
        self.components = {}

    def add_component(self, name, component):
        self.components[name] = component

    def get_component(self, name):
        return self.components.get(name)

    def update(self):
        for component in self.components.values():
            if hasattr(component, 'update'):
                component.update()