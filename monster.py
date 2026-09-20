from game_data import MONSTER_DATA

# this is going to only be data so no need for pygame
class Monster:
    def __init__(self, name, level):
        self.name, self.level = name, level

        # stats
        self.stats = MONSTER_DATA[name]['stats']
        self.base_stats = MONSTER_DATA[name]['stats']

    def __repr__(self):
        return f'monster: {self.name}, lvl: {self.level}'
