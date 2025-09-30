from ..components.item import Item

class Weapon(Item):
    def __init__(self, name, description, damage, icon_color=(200, 50, 50)):
        super().__init__(name, description, icon_color)
        self.damage = damage

    def use(self, player):
        # Implement weapon use logic
        pass