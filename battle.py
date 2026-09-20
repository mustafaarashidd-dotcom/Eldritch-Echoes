from settings import *
from sprites import MonsterSprite, MonsterNameSprite, PlayerStatsSprite, PlayerSprite, AttackSprite
from game_data import PLAYER_DATA, ENEMY_DATA, MONSTER_DATA, ATTACK_DATA
import random
from AccountDatabase import change_damage_taken

class Battle:
    def __init__(self, opposing_monster, opposing_monster_surf, font, game_instance, monster_frames, sounds):
        self.display_surface = pygame.display.get_surface()
        self.opposing_monster = opposing_monster
        self.opposing_monster_surf = opposing_monster_surf
        self.font = font
        self.game_instance = game_instance
        self.monster_frames = monster_frames
        self.sounds = sounds

        # timers and conditional selection variables
        self.selecting = True  # This is used to vary if the player should be drawn or not
        self.combat_index = -1  # The number representing the attack from NPC (e.g. 0 for the first attack,
        # 1 for the second attack)
        self.enemy_attack = False
        self.act_dialog = False
        self.inventory_dialog = False
        self.fight = False
        self.defeated_dialog = False
        self.act_timer = None
        self.act_display_duration = 5000  # milliseconds (3 seconds)
        self.enemy_attack_timer = None  # This is to check if the enemies attack has been going on for 10 seconds,
                                        # if true then it stops the attack and outputs the dialog allowing the player to select again
        self.enemy_attack_duration = 10000  # (10 seconds)
        self.kill = False
        self.spare = False
        self.flag = False
        self.death_timer = None
        self.attack_timer = None  # This is to delay all the projectiles in the attacks

        self.battle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.opponent_sprites = pygame.sprite.Group()

        self.opposing_monster_surf = pygame.transform.scale(self.opposing_monster_surf, (60, 60)).convert_alpha()

        # button dimensions
        self.main_rect = pygame.FRect(265, 615, 750, 75)

        self.items = {
            0: 'FIGHT',
            1: 'ACT',
            2: 'INVENTORY',
            3: 'FLEE'
        }

        # list
        self.columns = 4
        self.list_width = self.main_rect.width / self.columns
        self.item_height = self.main_rect.height
        self.index = 0
        self.selected_index = None

        # movement
        self.direction = vector()
        self.player_pos_x = 635
        self.player_pos_y = 405

        # character key to access enemy data
        if self.opposing_monster.name == 'animal':
            self.key = 'o1'
        elif self.opposing_monster.name == 'shark':
            self.key = 'o2'
        elif self.opposing_monster.name == 'captain_dreadful':
            self.key = 'o3'
        elif self.opposing_monster.name == 'spirit':
            self.key = 'o4'
        elif self.opposing_monster.name == 'captain_marduk':
            self.key = 'o5'

        # Enemy Attack Variables
        self.stars = []
        self.star_count = 0
        self.star_add_increment = 1500
        self.clock = pygame.time.Clock()
        self.star_vel = 6
        self.lines_top = []
        self.lines_bottom = []
        self.line_add_increment = 1500
        self.line_count = 0
        self.line_vel = 4
        self.ping_pong_1_x_velocity = 2
        self.ping_pong_1_y_velocity = 2
        self.ping_pong_2_x_velocity = 2
        self.ping_pong_2_y_velocity = -2
        self.ping_pong_3_x_velocity = 6
        self.ping_pong_3_y_velocity = 1
        self.ping_pong_1 = pygame.Rect((285, 245), (20, 20))
        self.ping_pong_2 = pygame.Rect((285, 558), (20, 20))
        self.ping_pong_3 = pygame.Rect((285, 370), (20, 20))
        self.ping_pongs_1 = []
        self.ping_pongs_2 = []
        self.ping_pongs_3 = []

    def dialog(self):
        max_index = len(ENEMY_DATA[self.key]['dialog']['combat_dialog'])-1
        if self.combat_index <= max_index:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][self.combat_index]
            text_surf = self.font.render(text, False, 'white')
        else:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][max_index]
            text_surf = self.font.render(text, False, 'white')
        text_rect = text_surf.get_frect(topleft=(295, 250))
        self.display_surface.blit(text_surf, text_rect)

        max_index = len(ENEMY_DATA[self.key]['dialog']['combat_dialog']) - 1
        if self.combat_index <= max_index:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][self.combat_index]
            text_surf = self.font.render(text, False, 'white')
        else:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][max_index]
            text_surf = self.font.render(text, False, 'white')
        text_rect = text_surf.get_frect(topleft=(295, 250))
        self.display_surface.blit(text_surf, text_rect)

        max_index = len(ENEMY_DATA[self.key]['dialog']['combat_dialog']) - 1
        if self.combat_index <= max_index:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][self.combat_index]
            text_surf = self.font.render(text, False, 'white')
        else:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][max_index]
            text_surf = self.font.render(text, False, 'white')
        text_rect = text_surf.get_frect(topleft=(295, 250))
        self.display_surface.blit(text_surf, text_rect)

        max_index = len(ENEMY_DATA[self.key]['dialog']['combat_dialog']) - 1
        if self.combat_index <= max_index:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][self.combat_index]
            text_surf = self.font.render(text, False, 'white')
        else:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][max_index]
            text_surf = self.font.render(text, False, 'white')
        text_rect = text_surf.get_frect(topleft=(295, 250))
        self.display_surface.blit(text_surf, text_rect)

        max_index = len(ENEMY_DATA[self.key]['dialog']['combat_dialog']) - 1
        if self.combat_index <= max_index:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][self.combat_index]
            text_surf = self.font.render(text, False, 'white')
        else:
            text = ENEMY_DATA[self.key]['dialog']['combat_dialog'][max_index]
            text_surf = self.font.render(text, False, 'white')
        text_rect = text_surf.get_frect(topleft=(295, 250))
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):
        # border
        rect_position = (315, 225)
        rect_size = (750, 360)
        rect_position = ((1280-rect_size[0])/2, rect_position[1])  # so that its always evenly in the middle
        border_thickness = 5
        self.border = pygame.draw.rect(self.display_surface, 'white', (rect_position, rect_size), border_thickness)

        # Create four border rectangles (top, bottom, left, right)
        self.top_border = pygame.Rect(rect_position[0], rect_position[1], rect_size[0], border_thickness)
        self.bottom_border = pygame.Rect(rect_position[0], rect_position[1] + rect_size[1] - border_thickness,
                                    rect_size[0], border_thickness)
        self.left_border = pygame.Rect(rect_position[0], rect_position[1], border_thickness, rect_size[1])
        self.right_border = pygame.Rect(rect_position[0] + rect_size[0] - border_thickness, rect_position[1],
                                   border_thickness, rect_size[1])

        # player
        self.player_surf = pygame.image.load('battle_icons/player.png')
        self.player_stats = PLAYER_DATA['stats']
        self.player_max_stats = PLAYER_DATA['max_stats']
        bar_pos = (815, 589)
        self.player_pos = (self.player_pos_x, self.player_pos_y)
        self.player_sprite = PlayerSprite(self.player_pos, bar_pos, self.player_surf, self.player_sprites, self.player_stats, self.player_max_stats, self.font)
        if self.selecting is False and self.defeated_dialog is False:
            self.display_surface.blit(self.player_sprite.image, self.player_sprite.rect)

        # opponent
        pos = (self.border.midtop[0], self.border.midtop[1]-100)
        groups = (self.battle_sprites, self.player_sprites)
        self.monster_sprite = MonsterSprite(pos, self.opposing_monster_surf, groups, self.opposing_monster.name, self.opposing_monster.level)

        # name and level
        name_pos = (self.border.left, self.border.bottom+2)
        MonsterNameSprite(name_pos, self.monster_sprite, self.font)

    def buttons(self):
        bg_rect = pygame.FRect(self.main_rect.topleft, (self.list_width, self.item_height))
        pygame.draw.rect(self.display_surface, 'black', bg_rect)

        v_offset = 0 if self.index < self.columns else -(self.index - self.columns + 1) * self.list_width
        for index, item in self.items.items():
            # colors
            if self.index != index:
                bg_color = 'orange'
                text_color = 'orange'
            else:
                bg_color = 'white'
                text_color = 'white'

            left = self.main_rect.left + index * self.list_width + v_offset  # depending on index, the top will be lower and lower
            item_rect = pygame.draw.rect(self.display_surface, 'orange', (left, self.main_rect.top, self.list_width, self.item_height), 5)
            text_surf = self.font.render(item, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(45, 0))

            if item_rect.colliderect(self.main_rect):
                pygame.draw.rect(self.display_surface, bg_color, (left, self.main_rect.top, self.list_width, self.item_height), 5)

                self.display_surface.blit(text_surf, text_rect)

            for i in range(min(self.columns, len(self.items))):
                top = self.main_rect.top
                bottom = self.main_rect.bottom
                x = self.main_rect.left + self.list_width * i
                pygame.draw.line(self.display_surface, 'black', (x, top), (x, bottom), 3)

    def input(self, dt):
        self.keys = pygame.key.get_just_pressed()
        if self.keys[pygame.K_LEFT] and self.selecting:
            self.index -= 1
        if self.keys[pygame.K_RIGHT] and self.selecting:
            self.index += 1
        if self.keys[pygame.K_SPACE] and self.selecting:
            self.selected_index = self.index
            if self.selected_index == 0:
                # fight (hit the enemy)
                if self.opposing_monster.name != "spirit" and self.opposing_monster.name != "captain_marduk":
                    if self.game_instance.equipped_weapon == "Cannon Balls":
                        self.apply_attack_animation(self.monster_sprite, 'fire', 'explosion', dt)
                    else:
                        self.apply_attack_animation(self.monster_sprite, 'sword', 'scratch', dt)
                    self.fight = True
                    AT_damage = self.player_sprite.AT - MONSTER_DATA[self.opposing_monster.name]['stats']['DF']
                    MONSTER_DATA[self.opposing_monster.name]['stats']['HP'] -= AT_damage
                    self.selecting = False
                    self.fight = False
                    self.combat_index += 1
                    self.enemy_attack_timer = pygame.time.get_ticks()
                    self.attack_timer = pygame.time.get_ticks()
                    self.enemy_attack = True

                    if MONSTER_DATA[self.opposing_monster.name]['stats']['HP'] <= 0:
                        self.defeated_dialog = True
                        self.selecting = False
                        self.fight = False
                        self.flag = True
                        self.enemy_attack = False

                elif self.opposing_monster.name != "captain_marduk":
                    # spirit
                    if self.game_instance.equipped_weapon == "Cannon Balls":
                        self.apply_attack_animation(self.monster_sprite, 'fire', 'explosion', dt)
                    else:
                        self.apply_attack_animation(self.monster_sprite, 'sword', 'scratch', dt)
                    self.fight = True
                    self.selecting = False
                    self.fight = False
                    self.combat_index += 1
                    self.enemy_attack_timer = pygame.time.get_ticks()
                    self.attack_timer = pygame.time.get_ticks()
                    self.enemy_attack = True

                    if self.combat_index == 5:
                        self.defeated_dialog = True
                        self.enemy_attack = False
                        self.selecting = False
                        self.fight = False
                        self.flag = True

                elif self.opposing_monster.name != "spirit":
                    # captain marduk
                    if self.game_instance.equipped_weapon == "Cannon Balls":
                        self.apply_attack_animation(self.monster_sprite, 'fire', 'explosion', dt)
                    else:
                        self.apply_attack_animation(self.monster_sprite, 'sword', 'scratch', dt)
                    self.fight = True
                    AT_damage = self.player_sprite.AT - MONSTER_DATA[self.opposing_monster.name]['stats']['DF']
                    MONSTER_DATA[self.opposing_monster.name]['stats']['HP'] -= AT_damage
                    self.selecting = False
                    self.fight = False
                    self.combat_index += 1
                    self.enemy_attack_timer = pygame.time.get_ticks()
                    self.attack_timer = pygame.time.get_ticks()
                    self.enemy_attack = True

                    if MONSTER_DATA[self.opposing_monster.name]['stats']['HP'] <= 0:
                        self.defeated_dialog = True
                        self.selecting = False
                        self.fight = False
                        self.flag = True
                        self.enemy_attack = False

            elif self.selected_index == 1:
                self.act_dialog = True

                # act (check the enemy stats)
                self.act_timer = pygame.time.get_ticks()
                self.HP_text_surf = self.font.render("HP:  "+str(MONSTER_DATA[self.opposing_monster.name]['stats']['HP']), False, 'white')
                self.DF_text_surf = self.font.render("DF:  "+str(MONSTER_DATA[self.opposing_monster.name]['stats']['DF']), False, 'white')
                self.AT_text_surf = self.font.render("AT:  "+str(MONSTER_DATA[self.opposing_monster.name]['stats']['AT']), False, 'white')
                self.SPEED_text_surf = self.font.render("SPEED:  "+str(MONSTER_DATA[self.opposing_monster.name]['stats']['SPEED']), False, 'white')
                self.EXP_text_surf = self.font.render("EXP:  "+str(MONSTER_DATA[self.opposing_monster.name]['stats']['EXP']), False, 'white')
                if self.opposing_monster.name == "spirit":
                    self.taunt_text_surf = self.font.render("He'll keep dodging, outlast him", False, 'white')
                elif self.opposing_monster.name == 'captain_marduk':
                    self.taunt_text_surf = self.font.render("This is the final fight", False, 'white')
                else:
                    self.taunt_text_surf = self.font.render("Try not to get hit!", False, 'white')
                self.HP_text_rect = self.HP_text_surf.get_frect(topleft=(295, 250))
                self.DF_text_rect = self.DF_text_surf.get_frect(topleft=(295, self.HP_text_rect.bottom+5))
                self.AT_text_rect = self.AT_text_surf.get_frect(topleft=(295, self.DF_text_rect.bottom+5))
                self.SPEED_text_rect = self.SPEED_text_surf.get_frect(topleft=(295, self.AT_text_rect.bottom+5))
                self.EXP_text_rect = self.EXP_text_surf.get_frect(topleft=(295, self.SPEED_text_rect.bottom+5))
                self.taunt_text_rect = self.taunt_text_surf.get_frect(topleft=(295, self.EXP_text_rect.bottom+10))


            elif self.selected_index == 2:
                # item (check your consumables and use one automatically)
                self.inventory_dialog = True
                max_index = len(self.game_instance.inventory_dict)-1

                if max_index == 0:
                    self.selecting = False
                    self.inventory_dialog = False
                    self.combat_index += 1
                    self.enemy_attack_timer = pygame.time.get_ticks()
                    self.attack_timer = pygame.time.get_ticks()
                    self.enemy_attack = True

                if max_index == 1:
                    if self.game_instance.inventory_dict[1] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    else:
                        self.selecting = False
                        self.inventory_dialog = False
                        self.combat_index += 1
                        self.enemy_attack_timer = pygame.time.get_ticks()
                        self.attack_timer = pygame.time.get_ticks()
                        self.enemy_attack = True

                elif max_index == 2:
                    if self.game_instance.inventory_dict[2] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.combat_index += 1
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[1] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    else:
                        self.selecting = False
                        self.inventory_dialog = False
                        self.combat_index += 1
                        self.enemy_attack_timer = pygame.time.get_ticks()
                        self.attack_timer = pygame.time.get_ticks()
                        self.enemy_attack = True

                elif max_index == 3:
                    if self.game_instance.inventory_dict[3] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[2] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.combat_index += 1
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[1] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    else:
                        self.selecting = False
                        self.inventory_dialog = False
                        self.combat_index += 1
                        self.enemy_attack_timer = pygame.time.get_ticks()
                        self.attack_timer = pygame.time.get_ticks()
                        self.enemy_attack = True

                elif max_index == 4:
                    if self.game_instance.inventory_dict[4] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[4]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[4]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[3] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[2] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.combat_index += 1
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[1] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    else:
                        self.selecting = False
                        self.inventory_dialog = False
                        self.combat_index += 1
                        self.enemy_attack_timer = pygame.time.get_ticks()
                        self.attack_timer = pygame.time.get_ticks()
                        self.enemy_attack = True

                elif max_index == 5:
                    if self.game_instance.inventory_dict[5] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[5]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[5]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[4] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[4]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[4]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[3] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[2] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.combat_index += 1
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[1] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    else:
                        self.selecting = False
                        self.inventory_dialog = False
                        self.combat_index += 1
                        self.enemy_attack_timer = pygame.time.get_ticks()
                        self.attack_timer = pygame.time.get_ticks()
                        self.enemy_attack = True

                elif max_index == 6:
                    if self.game_instance.inventory_dict[6] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[6]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[6]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    if self.game_instance.inventory_dict[5] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[5]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[5]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[4] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[4]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[4]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[3] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[3]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[2] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.combat_index += 1
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[2]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    elif self.game_instance.inventory_dict[1] == 'Consumable':
                        self.sounds['heal'].play()
                        if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                            PLAYER_DATA['stats']['HP'] += 15
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                        else:
                            PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                            del self.game_instance.inventory_dict[1]
                            if len(self.game_instance.inventory_dict) > 1:
                                self.game_instance.inventory_dict = {i: v for i, v in enumerate(
                                    self.game_instance.inventory_dict.values())}
                            self.selecting = False
                            self.inventory_dialog = False
                            self.combat_index += 1
                            self.enemy_attack_timer = pygame.time.get_ticks()
                            self.attack_timer = pygame.time.get_ticks()
                            self.enemy_attack = True
                    else:
                        self.selecting = False
                        self.inventory_dialog = False
                        self.combat_index += 1
                        self.enemy_attack_timer = pygame.time.get_ticks()
                        self.attack_timer = pygame.time.get_ticks()
                        self.enemy_attack = True
            else:
                # Flee (leave combat)
                ENEMY_DATA[self.key]['in_combat'] = False
                MONSTER_DATA[self.opposing_monster.name]['stats']['HP'] = MONSTER_DATA[self.opposing_monster.name]['base_stats']['HP']
                self.game_instance.battle = None
                self.game_instance.battle_music_playing = False
                self.game_instance.spirit_battle_music_playing = False
                self.game_instance.marduk_battle_music_playing = False
                self.game_instance.battle_music.stop()
                self.game_instance.spirit_battle_music.stop()
                self.game_instance.marduk_battle_music.stop()

        self.index = self.index % len(self.items)

        if self.selecting is False:
            self.move_keys = pygame.key.get_pressed()
            self.input_vector = vector()
            if self.move_keys[pygame.K_UP] or self.move_keys[pygame.K_w]:
                self.input_vector.y -= 1
            if self.move_keys[pygame.K_DOWN] or self.move_keys[pygame.K_s]:
                self.input_vector.y += 1
            if self.move_keys[pygame.K_LEFT] or self.move_keys[pygame.K_a]:
                self.input_vector.x -= 1
            if self.move_keys[pygame.K_RIGHT] or self.move_keys[pygame.K_d]:
                self.input_vector.x += 1
            self.direction = self.input_vector

    def move(self, dt):
        self.hitbox = self.player_sprite.rect.inflate(-6, -6)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.player_pos_x += self.direction.x * 350 * dt
        self.hitbox.centerx = self.player_sprite.rect.centerx
        self.collisions('horizontal')

        self.player_pos_y += self.direction.y * 350 * dt
        self.hitbox.centery = self.player_sprite.rect.centery
        self.collisions('vertical')

    def collisions(self, axis):
        if axis == 'horizontal':
            if self.player_sprite.rect.colliderect(self.right_border):
                # Prevent movement past the right border
                self.player_sprite.rect.right = self.right_border.left
                self.player_pos_x = self.player_sprite.rect.centerx
            elif self.player_sprite.rect.colliderect(self.left_border):
                # Prevent movement past the left border
                self.player_sprite.rect.left = self.left_border.right
                self.player_pos_x = self.player_sprite.rect.centerx

        # Check vertical collisions
        elif axis == 'vertical':
            if self.player_sprite.rect.colliderect(self.bottom_border):
                # Prevent movement past the bottom border
                self.player_sprite.rect.bottom = self.bottom_border.top
                self.player_pos_y = self.player_sprite.rect.centery
            elif self.player_sprite.rect.colliderect(self.top_border):
                # Prevent movement past the top border
                self.player_sprite.rect.top = self.top_border.bottom
                self.player_pos_y = self.player_sprite.rect.centery

    def apply_attack_animation(self, target_sprite, attack_sound, attack, dt):
        AttackSprite(target_sprite.rect.center, self.monster_frames['attacks'][ATTACK_DATA[attack]['animation']], self.battle_sprites)
        self.sounds[attack_sound].play()
        self.sounds[attack_sound].set_volume(0.15)

    def draw_stats(self):
        self.display_surface.blit(self.HP_text_surf, self.HP_text_rect)
        self.display_surface.blit(self.DF_text_surf, self.DF_text_rect)
        self.display_surface.blit(self.AT_text_surf, self.AT_text_rect)
        self.display_surface.blit(self.SPEED_text_surf, self.SPEED_text_rect)
        self.display_surface.blit(self.EXP_text_surf, self.EXP_text_rect)
        self.display_surface.blit(self.taunt_text_surf, self.taunt_text_rect)

    def update(self, dt):
        # Battle Music
        if self.game_instance.spirit_battle_music_playing is False and self.opposing_monster.name == 'spirit':
            self.game_instance.spirit_battle_music.play(-1)
            self.game_instance.spirit_battle_music.set_volume(0.6)
            self.game_instance.spirit_battle_music_playing = True
        elif self.game_instance.marduk_battle_music_playing is False and self.opposing_monster.name == 'captain_marduk':
            self.game_instance.marduk_battle_music.play(-1)
            self.game_instance.marduk_battle_music.set_volume(0.6)
            self.game_instance.marduk_battle_music_playing = True
        elif self.game_instance.battle_music_playing is False and self.opposing_monster.name != 'spirit' and self.opposing_monster.name != 'captain_marduk':
            self.game_instance.battle_music.play(-1)
            self.game_instance.battle_music.set_volume(1.5)
            self.game_instance.battle_music_playing = True

        # Updating screen and methods
        self.display_surface.fill('black')
        self.setup()
        self.battle_sprites.draw(self.display_surface)
        self.battle_sprites.update(dt)
        self.input(dt)
        self.move(dt)

        # Death screen

        if PLAYER_DATA['stats']['HP'] <= 0:
            self.game_instance.battle_music_playing = False
            self.game_instance.spirit_battle_music_playing = False
            self.game_instance.marduk_battle_music_playing = False
            self.game_instance.battle_music.stop()
            self.game_instance.spirit_battle_music.stop()
            self.game_instance.marduk_battle_music.stop()
            self.enemy_attack = False
            self.selecting = False
            MONSTER_DATA[self.opposing_monster.name]['stats']['HP'] = MONSTER_DATA[self.opposing_monster.name]['base_stats']['HP']
            text_surf = self.font.render("GAME OVER", False, 'White')
            text_rect = text_surf.get_frect(center=(GAME_SCREEN_WIDTH/2, GAME_SCREEN_HEIGHT/2))
            self.display_surface.blit(text_surf, text_rect)
            if pygame.time.get_ticks() - self.death_timer >= 4000:
                ENEMY_DATA[self.key]['in_combat'] = False
                self.game_instance.battle = None
                PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']/2

        # Buttons

        if self.selecting and self.act_dialog is False and self.inventory_dialog is False and self.fight is False and self.defeated_dialog is False:
            self.dialog()
            self.buttons()

        # Act screen

        if self.act_dialog:
            self.draw_stats()
            if pygame.time.get_ticks() - self.act_timer > self.act_display_duration:
                self.act_dialog = False
                self.selecting = False
                self.combat_index += 1
                self.enemy_attack_timer = pygame.time.get_ticks()
                self.attack_timer = pygame.time.get_ticks()
                self.enemy_attack = True

        # Kill or spare

        if self.defeated_dialog:
            self.game_instance.battle_music_playing = False
            self.game_instance.spirit_battle_music_playing = False
            self.game_instance.marduk_battle_music_playing = False
            self.game_instance.battle_music.stop()
            self.game_instance.spirit_battle_music.stop()
            self.game_instance.marduk_battle_music.stop()
            Y_N_text = "Press the Y key to kill, the N key to spare"
            Y_N_text_surf = self.font.render(Y_N_text, False, 'white')
            Y_N_text_rect = Y_N_text_surf.get_frect(topleft=(295, 250))
            self.display_surface.blit(Y_N_text_surf, Y_N_text_rect)
            if self.flag:
                if (self.kill is False or self.spare is False) and self.opposing_monster.name != 'captain_marduk':
                    if self.keys[pygame.K_y]:
                        PLAYER_DATA['stats']['EXP'] += 1
                        self.kill = True
                        ENEMY_DATA[self.key]['killed'] = True
                        ENEMY_DATA[self.key]['defeated'] = True
                    elif self.keys[pygame.K_n]:
                        self.spare = True
                        ENEMY_DATA[self.key]['spared'] = True
                        ENEMY_DATA[self.key]['defeated'] = True
                else:
                    # Captain Marduk final route (game ending)
                    change_damage_taken(self.game_instance.accountDetails[0], self.game_instance.damage)
                    if self.keys[pygame.K_y]:
                        PLAYER_DATA['stats']['EXP'] += 1
                        self.kill = True
                        # determine using players exp
                        if PLAYER_DATA['stats']['EXP'] < 5:
                            # neutral
                            ENEMY_DATA[self.key]['defeated'] = True
                            ENEMY_DATA[self.key]['killed'] = True
                            ENEMY_DATA[self.key]['neutral'] = True
                        else:
                            # genocide
                            ENEMY_DATA[self.key]['defeated'] = True
                            ENEMY_DATA[self.key]['killed'] = True
                            ENEMY_DATA[self.key]['genocide'] = True
                    elif self.keys[pygame.K_n]:
                        self.spare = True
                        # determine using players exp
                        if PLAYER_DATA['stats']['EXP'] == 0:
                            # pacifist
                            ENEMY_DATA[self.key]['defeated'] = True
                            ENEMY_DATA[self.key]['spared'] = True
                            ENEMY_DATA[self.key]['pacifist'] = True
                        else:
                            # neutral
                            ENEMY_DATA[self.key]['defeated'] = True
                            ENEMY_DATA[self.key]['spared'] = True
                            ENEMY_DATA[self.key]['neutral'] = True
            if ENEMY_DATA[self.key]['defeated']:
                ENEMY_DATA[self.key]['in_combat'] = False
                self.game_instance.battle = None
                self.game_instance.battle_music_playing = False
                self.game_instance.spirit_battle_music_playing = False
                self.game_instance.marduk_battle_music_playing = False
                self.game_instance.battle_music.stop()
                self.game_instance.spirit_battle_music.stop()
                self.game_instance.marduk_battle_music.stop()

        # First Attacks

        if self.combat_index == 0 and self.enemy_attack:
            self.player_sprite.x = 635
            self.player_sprite.y = 405
            self.star_count += self.clock.tick(60)
            if self.star_count > self.star_add_increment:
                for _ in range(3):
                    star_y = random.randint(self.border.top, self.border.bottom - 20)
                    star = pygame.Rect((self.border.right - 20, star_y), (20, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.stars.append(star)
                        self.sounds['fireball'].play()
                        self.sounds['fireball'].set_volume(0.1)
                    # star add increment is already 1500 so it is that value for this attack
                    self.star_count = 0

            for star in self.stars[:]:
                star.x -= self.star_vel
                if star.x <= self.border.left:
                    self.stars.remove(star)
                elif star.x >= self.player_sprite.rect.x and star.colliderect(self.player_sprite.rect):
                    self.stars.remove(star)
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for star in self.stars:
                pygame.draw.rect(self.display_surface, "White", star)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.stars.clear()

        # Second Attacks

        elif self.combat_index == 1 and self.enemy_attack and self.opposing_monster.name != 'spirit' and self.opposing_monster.name != 'captain_marduk':
            self.player_sprite.x = 635
            self.player_sprite.y = 405
            self.star_count += self.clock.tick(60)
            if self.star_count > self.star_add_increment:
                for _ in range(3):
                    star_y = random.randint(self.border.top, self.border.bottom - 20)
                    star = pygame.Rect((self.border.right - 20, star_y), (20, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.stars.append(star)
                        self.sounds['fireball'].play()
                        self.sounds['fireball'].set_volume(0.1)
                    self.star_add_increment = 1000
                    self.star_count = 0

            for star in self.stars[:]:
                star.x -= self.star_vel
                if star.x <= self.border.left:
                    self.stars.remove(star)
                elif star.x >= self.player_sprite.rect.x and star.colliderect(self.player_sprite.rect):
                    self.stars.remove(star)
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for star in self.stars:
                pygame.draw.rect(self.display_surface, "White", star)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.stars.clear()

        elif self.combat_index == 1 and self.enemy_attack:
            # spirit and captain marduks second attack
            self.player_sprite.x = 635
            self.player_sprite.y = 405
            self.star_count += self.clock.tick(60)
            if self.star_count > self.star_add_increment:
                for _ in range(4):
                    star_y = random.randint(self.border.top, self.border.bottom - 20)
                    star = pygame.Rect((self.border.left + 20, star_y), (20, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.stars.append(star)
                        self.sounds['fireball'].play()
                        self.sounds['fireball'].set_volume(0.1)
                    self.star_add_increment = 400
                    self.star_count = 0

            for star in self.stars[:]:
                star.x += self.star_vel
                if star.x >= self.border.right - 20:
                    self.stars.remove(star)
                elif star.x <= self.player_sprite.rect.x and star.colliderect(self.player_sprite.rect):
                    self.stars.remove(star)
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for star in self.stars:
                pygame.draw.rect(self.display_surface, "White", star)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.stars.clear()

        # Third attacks

        elif self.combat_index == 2 and self.enemy_attack and self.opposing_monster.name != 'spirit' and self.opposing_monster.name != 'captain_marduk':
            self.player_sprite.x = 635
            self.player_sprite.y = 405
            self.star_count += self.clock.tick(60)
            if self.star_count > self.star_add_increment:
                for _ in range(3):
                    star_y = random.randint(self.border.top, self.border.bottom - 20)
                    star = pygame.Rect((self.border.right - 20, star_y), (20, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.stars.append(star)
                        self.sounds['fireball'].play()
                        self.sounds['fireball'].set_volume(0.1)
                    self.star_add_increment = 500
                    self.star_count = 0

            for star in self.stars[:]:
                star.x -= self.star_vel
                if star.x <= self.border.left:
                    self.stars.remove(star)
                elif star.x >= self.player_sprite.rect.x and star.colliderect(self.player_sprite.rect):
                    self.stars.remove(star)
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                  PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for star in self.stars:
                pygame.draw.rect(self.display_surface, "White", star)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.stars.clear()

        elif self.combat_index == 2 and self.enemy_attack:
            # circular attack (the lines either side) (only for spirit and captain marduk)
            self.line_count += self.clock.tick(60)
            if self.line_count > self.line_add_increment:
                for _ in range(1):
                    line1 = pygame.Rect((self.border.right - self.border.width/2, self.border.top - 10), (self.border.width/2, 10))
                    line2 = pygame.Rect((self.border.left, self.border.bottom + 10), (self.border.width/2, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.lines_top.append(line1)
                        self.lines_bottom.append(line2)
                        self.sounds['RandomAttackSoundEffect'].play()
                    self.line_add_increment = 1000
                    self.line_count = 0
            for line1 in self.lines_top[:]:
                line1.y += self.line_vel
                if line1.y >= self.border.bottom:
                    self.lines_top.remove(line1)
                elif line1.y <= self.player_sprite.rect.y and line1.colliderect(self.player_sprite.rect):
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()
            for line2 in self.lines_bottom[:]:
                line2.y -= self.line_vel
                if line2.y <= self.border.top:
                    self.lines_bottom.remove(line2)
                elif line2.y >= self.player_sprite.rect.y and line2.colliderect(self.player_sprite.rect):
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                  PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for line1 in self.lines_top:
                pygame.draw.rect(self.display_surface, 'white', line1)
            for line2 in self.lines_bottom:
                pygame.draw.rect(self.display_surface, 'white', line2)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.lines_top.clear()
                self.lines_bottom.clear()

        # Fourth attacks

        elif self.combat_index == 3 and self.enemy_attack and self.opposing_monster.name != 'spirit' and self.opposing_monster.name != 'captain_marduk':
            self.player_sprite.x = 635
            self.player_sprite.y = 405
            self.star_count += self.clock.tick(60)
            if self.star_count > self.star_add_increment:
                for _ in range(4):
                    star_y = random.randint(self.border.top, self.border.bottom - 20)
                    star = pygame.Rect((self.border.right - 20, star_y), (20, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.stars.append(star)
                        self.sounds['fireball'].play()
                        self.sounds['fireball'].set_volume(0.1)
                    self.star_add_increment = 500
                    self.star_count = 0

            for star in self.stars[:]:
                star.x -= self.star_vel
                if star.x <= self.border.left:
                    self.stars.remove(star)
                elif star.x >= self.player_sprite.rect.x and star.colliderect(self.player_sprite.rect):
                    self.stars.remove(star)
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                  PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                 PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for star in self.stars:
                pygame.draw.rect(self.display_surface, "White", star)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.stars.clear()

        elif self.combat_index == 3 and self.enemy_attack:
            self.player_sprite.x = 635
            self.player_sprite.y = 405
            self.star_count += self.clock.tick(60)
            if self.star_count > self.star_add_increment:
                for _ in range(3):
                    star_y = random.randint(self.border.top, self.border.bottom - 20)
                    star = pygame.Rect((self.border.right - 20, star_y), (20, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.stars.append(star)
                        self.sounds['fireball'].play()
                        self.sounds['fireball'].set_volume(0.1)
                    self.star_add_increment = 200
                    self.star_count = 0

            for star in self.stars[:]:
                star.x -= self.star_vel
                if star.x <= self.border.left:
                    self.stars.remove(star)
                elif star.x >= self.player_sprite.rect.x and star.colliderect(self.player_sprite.rect):
                    self.stars.remove(star)
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                  PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                 PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for star in self.stars:
                pygame.draw.rect(self.display_surface, "White", star)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.stars.clear()

        #  Fifth Attacks

        elif self.combat_index == 4 and self.enemy_attack and self.opposing_monster.name != 'captain_marduk' and self.opposing_monster.name != 'spirit':
            # Repeat attacks for the first 3 NPC's
            self.combat_index = 2

        elif self.combat_index == 4 and self.enemy_attack and self.opposing_monster.name != 'captain_marduk':
            # Spirits Fifth Attack
            self.line_count += self.clock.tick(60)
            if self.line_count > self.line_add_increment:
                for _ in range(1):
                    line1 = pygame.Rect((self.border.right - self.border.width / 2, self.border.bottom + 10),
                                        (self.border.width / 2, 10))
                    line2 = pygame.Rect((self.border.left, self.border.top - 10), (self.border.width / 2, 10))
                    if pygame.time.get_ticks() - self.attack_timer > 500:
                        self.lines_top.append(line2)
                        self.lines_bottom.append(line1)
                        self.sounds['RandomAttackSoundEffect'].play()
                    self.line_add_increment = 1000
                    self.line_count = 0
            for line1 in self.lines_top[:]:
                line1.y += self.line_vel
                if line1.y >= self.border.bottom:
                    self.lines_top.remove(line1)
                elif line1.y >= self.player_sprite.rect.y and line1.colliderect(self.player_sprite.rect):
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                 PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for line2 in self.lines_bottom[:]:
                line2.y -= self.line_vel
                if line2.y <= self.border.top:
                    self.lines_bottom.remove(line2)
                elif line2.y <= self.player_sprite.rect.y and line2.colliderect(self.player_sprite.rect):
                    self.sounds['hit'].play()
                    self.sounds['hit'].set_volume(0.1)
                    PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                  PLAYER_DATA['stats']['DF']
                    self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                                 PLAYER_DATA['stats']['DF']
                    self.death_timer = pygame.time.get_ticks()

            for line1 in self.lines_top:
                pygame.draw.rect(self.display_surface, 'white', line1)
            for line2 in self.lines_bottom:
                pygame.draw.rect(self.display_surface, 'white', line2)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.lines_top.clear()
                self.lines_bottom.clear()

        elif self.combat_index == 4 and self.enemy_attack:
            #  captain marduks fifth attack

            self.ping_pong_1.x += self.ping_pong_1_x_velocity
            self.ping_pong_2.x += self.ping_pong_2_x_velocity
            self.ping_pong_3.x += self.ping_pong_3_x_velocity
            self.ping_pong_1.y += self.ping_pong_1_y_velocity
            self.ping_pong_2.y += self.ping_pong_2_y_velocity
            self.ping_pong_3.y += self.ping_pong_3_y_velocity

            # deflections
            if self.ping_pong_1.colliderect(self.top_border) or self.ping_pong_1.colliderect(self.bottom_border):
                self.ping_pong_1_y_velocity *= -1
            if self.ping_pong_2.colliderect(self.top_border) or self.ping_pong_2.colliderect(self.bottom_border):
                self.ping_pong_2_y_velocity *= -1
            if self.ping_pong_3.colliderect(self.top_border) or self.ping_pong_3.colliderect(self.bottom_border):
                self.ping_pong_3_y_velocity *= -1
            if self.ping_pong_1.colliderect(self.left_border) or self.ping_pong_1.colliderect(self.right_border):
                self.ping_pong_1_x_velocity *= -1
            if self.ping_pong_2.colliderect(self.left_border) or self.ping_pong_2.colliderect(self.right_border):
                self.ping_pong_2_x_velocity *= -1
            if self.ping_pong_3.colliderect(self.left_border) or self.ping_pong_3.colliderect(self.right_border):
                self.ping_pong_3_x_velocity *= -1

            # player collisions
            if self.ping_pong_1.colliderect(self.player_sprite):
                self.sounds['hit'].play()
                self.sounds['hit'].set_volume(0.1)
                PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                              PLAYER_DATA['stats']['DF']
                self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                             PLAYER_DATA['stats']['DF']
                self.death_timer = pygame.time.get_ticks()
            elif self.ping_pong_2.colliderect(self.player_sprite):
                self.sounds['hit'].play()
                self.sounds['hit'].set_volume(0.1)
                PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                              PLAYER_DATA['stats']['DF']
                self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                             PLAYER_DATA['stats']['DF']
                self.death_timer = pygame.time.get_ticks()
            elif self.ping_pong_3.colliderect(self.player_sprite):
                self.sounds['hit'].play()
                self.sounds['hit'].set_volume(0.1)
                PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                              PLAYER_DATA['stats']['DF']
                self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                             PLAYER_DATA['stats']['DF']
                self.death_timer = pygame.time.get_ticks()
            if self.ping_pong_1.colliderect(self.player_sprite):
                self.sounds['hit'].play()
                self.sounds['hit'].set_volume(0.1)
                PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                              PLAYER_DATA['stats']['DF']
                self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                             PLAYER_DATA['stats']['DF']
                self.death_timer = pygame.time.get_ticks()
            elif self.ping_pong_2.colliderect(self.player_sprite):
                self.sounds['hit'].play()
                self.sounds['hit'].set_volume(0.1)
                PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                              PLAYER_DATA['stats']['DF']
                self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                             PLAYER_DATA['stats']['DF']
                self.death_timer = pygame.time.get_ticks()
            elif self.ping_pong_3.colliderect(self.player_sprite):
                self.sounds['hit'].play()
                self.sounds['hit'].set_volume(0.1)
                PLAYER_DATA['stats']['HP'] -= MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                              PLAYER_DATA['stats']['DF']
                self.game_instance.damage += MONSTER_DATA[self.opposing_monster.name]['stats']['AT'] - \
                                             PLAYER_DATA['stats']['DF']
                self.death_timer = pygame.time.get_ticks()

            for self.ping_pong_1 in self.ping_pongs_1[:]:
                pygame.draw.rect(self.display_surface, 'white', self.ping_pong_1)
            for self.ping_pong_2 in self.ping_pongs_2[:]:
                pygame.draw.rect(self.display_surface, 'white', self.ping_pong_2)
            for self.ping_pong_3 in self.ping_pongs_3[:]:
                pygame.draw.rect(self.display_surface, 'white', self.ping_pong_3)

            if pygame.time.get_ticks() - self.enemy_attack_timer > self.enemy_attack_duration:
                self.selecting = True
                self.direction = vector()
                self.enemy_attack = False
                self.ping_pongs_1.clear()
                self.ping_pongs_2.clear()
                self.ping_pongs_3.clear()
            else:
                self.ping_pongs_1.append(self.ping_pong_1)
                self.ping_pongs_2.append(self.ping_pong_2)
                self.ping_pongs_3.append(self.ping_pong_3)

        # repeat spirit and captain marduks last attacks or second last attack then last attack if the player does not select 'fight'
        # if they press 'fight' it will check for combat index 5 in the fight buttons selection further above in code
        elif self.combat_index == 5 and self.enemy_attack and self.opposing_monster.name != 'spirit':
            self.combat_index = 4

        elif self.combat_index == 5 and self.enemy_attack and self.opposing_monster.name != 'captain_marduk':

            self.combat_index = 3
