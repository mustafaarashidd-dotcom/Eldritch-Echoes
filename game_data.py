# Dialogs of all NPCs and their information (dialogs, defeated, stats[WIP], other things will gradually be added as well)
ENEMY_DATA = {
    'm1': {
        'dialog': {
            'default': ['Welcome player, this is the realm of pirates.', 'There is a missing treasure that is currently guarded'
                        ' by the king of all pirates', 'In this realm he and his strongest guard are said to have it', 'You have '
                        'been hired to find it', 'Your following tasks include: Find and defeat the animal, find and defeat the sharks.',
                        'Good luck!'],
            'complete': ['Well done! If you go to the ship you will travel to the next island.']},
        'gold': None,
        'looted_barrel': None,
        'looted_chest': None,
        'defeated': False,
        'complete': False,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'm2': {
        'dialog': {
            'default': ['Greetings, your following tasks include: Find and defeat captain Dreadful.'],
            'complete': ['Congratulations! If you go to the ship above me, you will travel to the next island.']},
        'gold': None,
        'looted_barrel': None,
        'looted_chest': None,
        'defeated': False,
        'complete': False,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'm3': {
        'dialog': {
            'default': ['Welcome, your following tasks include: Find and defeat the spirit of the island.'],
            'complete': ['Well done! If you go to the cave entrance somewhere on this island, you will travel to the final island.']},
        'gold': None,
        'looted_barrel': None,
        'looted_chest': None,
        'defeated': False,
        'complete': False,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'm4': {
        'dialog': {
            'default': ['Welcome, your following tasks include: Find and defeat captain Marduk, the king of the pirates in this realm.'],
            'complete': ['Congratulations! You finished the game, you got so far, if you wish to check how much health'
                         ' you lost throughout the whole game feel free to check for your account which is now appended to the leaderboard.']},
        'looted_chest': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': False,
        'complete': False,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'f1': {
        'dialog': {
            'default': ['Checkpoint Saved!']},
        'looted_chest': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': 'island_1',
        'killed': None
    },
    'f2': {
        'dialog': {
            'default': ['Checkpoint Saved!']},
        'looted_chest': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': 'island_2',
        'killed': None
    },
    'f3': {
        'dialog': {
            'default': ['Checkpoint Saved!']},
        'looted_chest': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': 'island_3',
        'killed': None
    },
    'f4': {
        'dialog': {
            'default': ['Checkpoint Saved!']},
        'looted_chest': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': 'island_4',
        'killed': None
    },
    'c1': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Consumable, Cost: 10)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Consumable',
        'looted_chest': False,
        'gold': 10,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'c2': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Cutlass, Cost: 5)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Cutlass',
        'looted_chest': False,
        'gold': 5,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'c3': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Consumable, Cost: 10)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Consumable',
        'looted_chest': False,
        'gold': 10,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'c4': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Leather Armour, Cost: 50)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Leather Armour',
        'looted_chest': False,
        'gold': 50,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'c5': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Cannon Balls, Cost: 30)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Cannon Balls',
        'looted_chest': False,
        'gold': 30,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'c6': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Consumable, Cost: 10)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Consumable',
        'looted_chest': False,
        'gold': 10,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'c7': {
        'dialog': {
            'default': ['Enter Y to purchase or ignore (Item: Metal Armour, Cost: 100)'],
            'already_looted': ['Item has already been looted'],
            'decline': ['Not enough gold']},
        'item': 'Metal Armour',
        'looted_chest': False,
        'gold': 100,
        'looted_barrel': None,
        'defeated': None,
        'complete': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'b1': {
        'dialog': {
            'default': ['Gold Collected: 10'],
            'already_looted': ['Gold has already been looted']},
        'gold': 10,
        'looted_barrel': False,
        'defeated': None,
        'complete': None,
        'looted_chest': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'b2': {
        'dialog': {
            'default': ['Gold Collected: 5'],
            'already_looted': ['Gold has already been looted']},
        'gold': 5,
        'looted_barrel': False,
        'defeated': None,
        'complete': None,
        'looted_chest': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'b3': {
        'dialog': {
            'default': ['Gold Collected: 40'],
            'already_looted': ['Gold has already been looted']},
        'gold': 40,
        'looted_barrel': False,
        'defeated': None,
        'complete': None,
        'looted_chest': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'b4': {
        'dialog': {
            'default': ['Gold Collected: 10'],
            'already_looted': ['Gold has already been looted']},
        'gold': 10,
        'looted_barrel': False,
        'defeated': None,
        'complete': None,
        'looted_chest': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'b5': {
        'dialog': {
            'default': ['Gold Collected: 90'],
            'already_looted': ['Gold has already been looted']},
        'gold': 90,
        'looted_barrel': False,
        'defeated': None,
        'complete': None,
        'looted_chest': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'b6': {
        'dialog': {
            'default': ['Gold Collected: 50'],
            'already_looted': ['Gold has already been looted']},
        'gold': 60,
        'looted_barrel': False,
        'defeated': None,
        'complete': None,
        'looted_chest': None,
        'enemy': False,
        'position': None,
        'killed': None
    },
    'o1': {
        'dialog': {
            'default': ['*growling*', 'FIGHT!'],
            'combat_dialog': ['*hissing*'],
            'defeated_spared': ['zzzzzzzz', 'woof!']},
        'looted_chest': None,
        'position': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': False,
        'complete': False,
        'killed': False,
        'spared': False,
        'enemy': True,
        'in_combat': False
    },
    'o2': {
        'dialog': {
            'default': ['*growling*', 'FIGHT!'],
            'combat_dialog': ['*chomp chomp chomp*'],
            'defeated_spared': ['zzzzzzzz']},
        'looted_chest': None,
        'position': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': False,
        'complete': False,
        'killed': False,
        'spared': False,
        'enemy': True,
        'in_combat': False
    },
    'o3': {
        'dialog': {
            'default': ['''ARRR, so you've came for the treasure! Too bad, I'll be getting it first. ''', 'FIGHT!'],
            'combat_dialog': ['Yarr!!!', '*Sword sharpening*'],
            'defeated_spared': ['''Yarr dammit! I'll never get the treasure...''',
                                '''How did I get defeated so easily... Heck, why'd you even spare me?!''']},
        'looted_chest': None,
        'position': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': False,
        'complete': False,
        'killed': False,
        'spared': False,
        'enemy': True,
        'in_combat': False
    },
    'o4': {
        'dialog': {
            'default': ['*Spooky noises*', 'FIGHT!'],
            'combat_dialog': ['Boo!', '*Crazy laugh*'],
            'defeated_spared': ['Fine whatever, you got me', '''Believe me, the king won't let you take the treasure that easily''']},
        'looted_chest': None,
        'position': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': False,
        'complete': False,
        'killed': False,
        'spared': False,
        'enemy': True,
        'in_combat': False
    },
    'o5': {
        'dialog': {
            'default': ['You must be the thief, im surprised you got passed the spirit', 'However, your journey ends here', 'FIGHT!'],
            'combat_dialog': ['. . .'],
            'pacifist_defeat': ['''This can't be, how have I been defeated *pant*, why are you sparing me?!''', 'TRAITORS!'],
            'neutral_defeat': ['''This can't be, how did you beat me so easily *cough* *cough*'''],
            'genocide_defeat': ['''NOOO!!!!''']},
        'looted_chest': None,
        'position': None,
        'gold': None,
        'looted_barrel': None,
        'defeated': False,
        'complete': False,
        'killed': False,
        'spared': False,
        'enemy': True,
        'pacifist': False,
        'genocide': False,
        'neutral': False,
        'in_combat': False
    },
    'null': {
        'dialog': ' ',
        'complete': True
    }
}

MONSTER_DATA = {
    'spirit': {
        'base_stats': {'HP': 1, 'AT': 20, 'DF': 0, 'SPEED': 100, 'EXP': 500},
        'stats': {'HP': 1, 'AT': 20, 'DF': 0, 'SPEED': 100, 'EXP': 500},
        'abilities': {0: 'blast', 5: 'obstacle_course'}
    },
    'captain_marduk': {
        'base_stats': {'HP': 150, 'AT': 25, 'DF': 20, 'SPEED': 20, 'EXP': 1000},
        'stats': {'HP': 150, 'AT': 25, 'DF': 20, 'SPEED': 20, 'EXP': 1000},
        'abilities': {0: 'slash', 5: 'cannon', 10: 'obstacle_course'}
    },
    'captain_dreadful': {
        'base_stats': {'HP': 60, 'AT': 20, 'DF': 4, 'SPEED': 10, 'EXP': 5},
        'stats': {'HP': 60, 'AT': 15, 'DF': 4, 'SPEED': 10, 'EXP': 5},
        'abilities': {0: 'slash', 5: 'cannon'}
    },
    'shark': {
        'base_stats': {'HP': 30, 'AT': 10, 'DF': 2, 'SPEED': 2, 'EXP': 2},
        'stats': {'HP': 30, 'AT': 10, 'DF': 2, 'SPEED': 2, 'EXP': 2},
        'abilities': {0: 'bite', 5: 'tooth_projectiles'}
    },
    'animal': {
        'base_stats': {'HP': 25, 'AT': 5, 'DF': 2, 'SPEED': 5, 'EXP': 1},
        'stats': {'HP': 25, 'AT': 5, 'DF': 2, 'SPEED': 5, 'EXP': 1},
        'abilities': {0: 'scratch', 5: 'bite'}
    }
}

PLAYER_DATA = {
    'max_stats': {'HP': 50},
    'stats': {'HP': 50, 'AT': 10, 'DF': 0, 'SPEED': 5, 'EXP': 0}
}

ATTACK_DATA = {
    'explosion': {'target': 'opponent', 'animation': 'explosion'},
    'scratch': {'target': 'opponent', 'animation': 'scratch'}
}
