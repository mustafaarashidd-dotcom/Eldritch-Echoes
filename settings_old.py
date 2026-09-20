# game setup
GAME_SCREEN_WIDTH = 1280
GAME_SCREEN_HEIGHT = 720
TILESIZE = 32

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
UI_FONT = 'joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
UI_BORDER_COLOR_ACTIVE = 'gold'

# enemy data
monster_data = {  # create dictionary of dictionary values for all monsters data
    'animal': {'health': 20, 'exp': 1, 'damage': 5, 'attack_sound': 'audio/attack/claw.wav'},
    'sharks': {'health': 35, 'exp': 2, 'damage': 10, 'attack_sound': 'audio/attack/claw.wav'},
    'captain_dreadful': {'health': 100, 'exp': 12, 'damage': 20, 'attack_sound': 'audio/attack/slash.wav'},
    'spirit': {'health': 1, 'exp': 50, 'damage': 35, 'attack_sound': 'audio/attack/hit.wav'},
    'captain_marduk': {'health': 200, 'exp': 6, 'damage': 40,'attack_sound': 'audio/attack/hit.wav'}
}
