from ..utils.constants import *

LEVEL_CONFIG = {
    'rooms': {
        'start': {
            'name': 'Starting Room',
            'description': 'A cozy room with a chest',
            'exits': {'north': 'outside'},
            'walls': [
                (0, 0, 300, 40),  # Left part of top wall
                (500, 0, 300, 40),  # Right part of top wall
                (0, WINDOW_HEIGHT-40, WINDOW_WIDTH, 40),  # Bottom
                (0, 0, 40, WINDOW_HEIGHT),  # Left
                (WINDOW_WIDTH-40, 0, 40, WINDOW_HEIGHT),  # Right
            ],
            'doors': [
                {
                    'x': 300,
                    'y': 0,
                    'width': 200,
                    'height': 40,
                    'target': 'outside',
                    'direction': 'north'
                }
            ]
        },
        'outside': {
            'name': 'Outside',
            'description': 'A garden with an old man',
            'exits': {'south': 'start', 'east': 'garden'},
            'walls': [
                (0, 0, WINDOW_WIDTH, 40),  # Top
                (0, WINDOW_HEIGHT-40, 300, 40),  # Left part of bottom
                (500, WINDOW_HEIGHT-40, 300, 40),  # Right part of bottom
                (0, 0, 40, WINDOW_HEIGHT),  # Left
                (WINDOW_WIDTH-40, 0, 40, 300),  # Top part of right
                (WINDOW_WIDTH-40, 500, 40, 100),  # Bottom part of right
            ],
            'doors': [
                {
                    'x': 300,
                    'y': WINDOW_HEIGHT-40,
                    'width': 200,
                    'height': 40,
                    'target': 'start',
                    'direction': 'south'
                },
                {
                    'x': WINDOW_WIDTH-40,
                    'y': 300,
                    'width': 40,
                    'height': 200,
                    'target': 'garden',
                    'direction': 'east'
                }
            ]
        },
        'garden': {
            'name': 'Garden',
            'description': 'A peaceful garden with flowers',
            'exits': {'west': 'outside'},
            'walls': [
                (0, 0, WINDOW_WIDTH, 40),  # Top
                (0, WINDOW_HEIGHT-40, WINDOW_WIDTH, 40),  # Bottom
                (0, 0, 40, 300),  # Top part of left
                (0, 500, 40, 100),  # Bottom part of left
                (WINDOW_WIDTH-40, 0, 40, WINDOW_HEIGHT),  # Right
            ],
            'doors': [
                {
                    'x': 0,
                    'y': 300,
                    'width': 40,
                    'height': 200,
                    'target': 'outside',
                    'direction': 'west'
                }
            ]
        }
    },
    'starting_room': 'start'
}