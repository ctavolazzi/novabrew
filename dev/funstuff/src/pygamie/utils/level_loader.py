from ..components.room import Room

class LevelLoader:
    @staticmethod
    def load_level(config):
        rooms = {}
        starting_room = config['starting_room']

        # Create rooms
        for room_id, room_data in config['rooms'].items():
            room = Room(
                name=room_data['name'],
                description=room_data['description'],
                exits=room_data['exits']
            )
            rooms[room_id] = room

        return rooms, starting_room

# Make sure to export the class
__all__ = ['LevelLoader']