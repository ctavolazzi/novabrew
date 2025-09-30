from ..components.item import Item

class Potion(Item):
    def __init__(self, name, description, heal_amount, icon_color=(50, 200, 50)):
        super().__init__(name, description, icon_color)
        self.heal_amount = heal_amount

    def use(self, player):
        # Implement healing logic
        pass