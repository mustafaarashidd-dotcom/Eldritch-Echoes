import pygame.transform
from settings import *
from game_data import PLAYER_DATA

class MiniMenu:
    def __init__(self, fonts, menu, game_instance):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.game_instance = game_instance
        self.items = {
            0: 'STATS',
            1: 'INVENTORY',
            2: 'MAIN MENU'
        }

        # tint surf
        self.tint_surf = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.tint_surf.set_alpha(200)

        # dimensions
        self.main_rect = pygame.FRect(0, 0, GAME_SCREEN_WIDTH * 0.6, GAME_SCREEN_HEIGHT * 0.8).move_to(center=(GAME_SCREEN_WIDTH / 2, GAME_SCREEN_HEIGHT / 2))

        # list
        self.rows = 3
        self.list_width = self.main_rect.width
        self.item_height = self.main_rect.height / self.rows
        self.index = 0
        self.selected_index = None

        self.menu = menu

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.index -= 1
        if keys[pygame.K_DOWN]:
            self.index += 1
        if keys[pygame.K_SPACE]:
            self.selected_index = self.index
            if self.selected_index == 0:
                self.game_instance.menu_open = False
                self.game_instance.stats_menu_open = True
            elif self.selected_index == 1:
                self.game_instance.menu_open = False
                self.game_instance.inventory_open = True
            else:
                self.menu()

        self.index = self.index % len(self.items)

    def display_list(self):
        bg_rect = pygame.FRect(self.main_rect.topleft, (self.list_width, self.main_rect.height))
        pygame.draw.rect(self.display_surface, (90, 157, 157), bg_rect)

        v_offset = 0 if self.index < self.rows else -(self.index - self.rows + 1) * self.item_height
        for index, item in self.items.items():
            # colors
            if self.index != index:
                bg_color = (90, 157, 157)
            else:
                bg_color = 'light gray'

            text_color = 'Black'

            top = self.main_rect.top + index * self.item_height + v_offset  # depending on index, the top will be lower and lower
            item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

            text_surf = self.fonts['regular2'].render(item, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(45, 0))

            if item_rect.colliderect(self.main_rect):
                pygame.draw.rect(self.display_surface, bg_color, item_rect)

                self.display_surface.blit(text_surf, text_rect)

        # lines
        for i in range(min(self.rows, len(self.items))):
            y = self.main_rect.top + self.item_height * i
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, 'black', (left, y), (right, y))

        # shadow
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top))

    def update(self, dt):
        self.input()
        self.display_surface.blit(self.tint_surf, (0, 0))
        self.display_list()

class Inventory:
    def __init__(self, fonts, game_instance):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.game_instance = game_instance

        # tint surf
        self.tint_surf = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.tint_surf.set_alpha(200)

        # dimensions
        self.main_rect = pygame.FRect(0, 0, GAME_SCREEN_WIDTH * 0.6, GAME_SCREEN_HEIGHT * 0.8).move_to(center=(GAME_SCREEN_WIDTH / 2, GAME_SCREEN_HEIGHT / 2))

        # list
        self.rows = 4
        self.list_width = self.main_rect.width
        self.item_height = self.main_rect.height / self.rows
        self.index = 0
        self.selected_index = None

    def inv_input(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_UP]:
            self.index -= 1
        if keys[pygame.K_DOWN]:
            self.index += 1
        if keys[pygame.K_SPACE]:
            self.selected_index = self.index
            if self.selected_index == 0:
                self.game_instance.equipped_weapon = 'Dagger'

            if self.selected_index == 1:
                if self.game_instance.inventory_dict[1] == 'Cannon Balls':
                    self.game_instance.equipped_weapon = 'Cannon Balls'
                elif self.game_instance.inventory_dict[1] == 'Cutlass':
                    self.game_instance.equipped_weapon = 'Cutlass'
                elif self.game_instance.inventory_dict[1] == 'Consumable':
                    if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP']-15:
                        PLAYER_DATA['stats']['HP'] += 15
                        del self.game_instance.inventory_dict[1]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                    else:
                        PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                        del self.game_instance.inventory_dict[1]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                elif self.game_instance.inventory_dict[1] == 'Leather Armour':
                    self.game_instance.equipped_armour = 'Leather Armour'
                elif self.game_instance.inventory_dict[1] == 'Metal Armour':
                    self.game_instance.equipped_armour = 'Metal Armour'

            if self.selected_index == 2:
                if self.game_instance.inventory_dict[2] == 'Cannon Balls':
                    self.game_instance.equipped_weapon = 'Cannon Balls'
                elif self.game_instance.inventory_dict[2] == 'Cutlass':
                    self.game_instance.equipped_weapon = 'Cutlass'
                elif self.game_instance.inventory_dict[2] == 'Consumable':
                    if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                        PLAYER_DATA['stats']['HP'] += 15
                        del self.game_instance.inventory_dict[2]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                    else:
                        PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                        del self.game_instance.inventory_dict[2]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                elif self.game_instance.inventory_dict[2] == 'Leather Armour':
                    self.game_instance.equipped_armour = 'Leather Armour'
                elif self.game_instance.inventory_dict[2] == 'Metal Armour':
                    self.game_instance.equipped_armour = 'Metal Armour'

            if self.selected_index == 3:
                if self.game_instance.inventory_dict[3] == 'Cannon Balls':
                    self.game_instance.equipped_weapon = 'Cannon Balls'
                elif self.game_instance.inventory_dict[3] == 'Cutlass':
                    self.game_instance.equipped_weapon = 'Cutlass'
                elif self.game_instance.inventory_dict[3] == 'Consumable':
                    if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                        PLAYER_DATA['stats']['HP'] += 15
                        del self.game_instance.inventory_dict[3]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                    else:
                        PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                        del self.game_instance.inventory_dict[3]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                elif self.game_instance.inventory_dict[3] == 'Leather Armour':
                    self.game_instance.equipped_armour = 'Leather Armour'
                else:
                    self.game_instance.equipped_armour = 'Metal Armour'

            if self.selected_index == 4:
                if self.game_instance.inventory_dict[4] == 'Cannon Balls':
                    self.game_instance.equipped_weapon = 'Cannon Balls'
                elif self.game_instance.inventory_dict[4] == 'Cutlass':
                    self.game_instance.equipped_weapon = 'Cutlass'
                elif self.game_instance.inventory_dict[4] == 'Consumable':
                    if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                        PLAYER_DATA['stats']['HP'] += 15
                        del self.game_instance.inventory_dict[4]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                    else:
                        PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                        del self.game_instance.inventory_dict[4]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                elif self.game_instance.inventory_dict[4] == 'Leather Armour':
                    self.game_instance.equipped_armour = 'Leather Armour'
                else:
                    self.game_instance.equipped_armour = 'Metal Armour'

            if self.selected_index == 5:
                if self.game_instance.inventory_dict[5] == 'Cannon Balls':
                    self.game_instance.equipped_weapon = 'Cannon Balls'
                elif self.game_instance.inventory_dict[5] == 'Cutlass':
                    self.game_instance.equipped_weapon = 'Cutlass'
                elif self.game_instance.inventory_dict[5] == 'Consumable':
                    if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                        PLAYER_DATA['stats']['HP'] += 15
                        del self.game_instance.inventory_dict[5]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                    else:
                        PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                        del self.game_instance.inventory_dict[5]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                elif self.game_instance.inventory_dict[5] == 'Leather Armour':
                    self.game_instance.equipped_armour = 'Leather Armour'
                else:
                    self.game_instance.equipped_armour = 'Metal Armour'

            if self.selected_index == 6:
                if self.game_instance.inventory_dict[6] == 'Cannon Balls':
                    self.game_instance.equipped_weapon = 'Cannon Balls'
                elif self.game_instance.inventory_dict[6] == 'Cutlass':
                    self.game_instance.equipped_weapon = 'Cutlass'
                elif self.game_instance.inventory_dict[6] == 'Consumable':
                    if PLAYER_DATA['stats']['HP'] <= PLAYER_DATA['max_stats']['HP'] - 15:
                        PLAYER_DATA['stats']['HP'] += 15
                        del self.game_instance.inventory_dict[6]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                    else:
                        PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                        del self.game_instance.inventory_dict[6]
                        if len(self.game_instance.inventory_dict) > 1:
                            self.game_instance.inventory_dict = {i: v for i, v in enumerate(self.game_instance.inventory_dict.values())}
                elif self.game_instance.inventory_dict[6] == 'Leather Armour':
                    self.game_instance.equipped_armour = 'Leather Armour'
                else:
                    self.game_instance.equipped_armour = 'Metal Armour'

        if keys[pygame.K_ESCAPE]:
            self.game_instance.inventory_open = False
            self.game_instance.player.blocked = not self.game_instance.player.blocked  # So player cant move while mini menu appears again

        self.index = self.index % len(self.game_instance.inventory_dict)

    def inv_display_list(self):
        bg_rect = pygame.FRect(self.main_rect.topleft, (self.list_width, self.main_rect.height))
        pygame.draw.rect(self.display_surface, (75, 75, 75), bg_rect)

        v_offset = 0 if self.index < self.rows else -(self.index - self.rows + 1) * self.item_height
        for index, item in self.game_instance.inventory_dict.items():
            # colors
            if self.index != index:
                bg_color = (75, 75, 75)
            else:
                bg_color = 'light gray'

            text_color = 'Black'

            top = self.main_rect.top + index * self.item_height + v_offset  # depending on index, the top will be lower and lower
            item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

            text_surf = self.fonts['regular2'].render(item, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(45, 0))

            if item_rect.colliderect(self.main_rect):
                pygame.draw.rect(self.display_surface, bg_color, item_rect)

                self.display_surface.blit(text_surf, text_rect)

        # lines
        for i in range(min(self.rows, len(self.game_instance.inventory_dict))):
            y = self.main_rect.top + self.item_height * i
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, 'black', (left, y), (right, y))

        # shadow
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top))

    def update(self):
        self.inv_input()
        self.display_surface.blit(self.tint_surf, (0, 0))
        self.inv_display_list()

class Stats_menu:
    def __init__(self, fonts, game_instance):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.game_instance = game_instance

        # tint surf
        self.tint_surf = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.tint_surf.set_alpha(200)

        # dimensions
        self.main_rect = pygame.FRect(0, 0, GAME_SCREEN_WIDTH * 0.6, GAME_SCREEN_HEIGHT * 0.8).move_to(
            center=(GAME_SCREEN_WIDTH / 2, GAME_SCREEN_HEIGHT / 2))

        # list
        self.rows = 5
        self.list_width = self.main_rect.width
        self.item_height = self.main_rect.height / self.rows
        self.index = 0
        self.selected_index = None

    def input(self):
        keys = pygame.key.get_just_pressed()

        self.items = {0: 'HEALTH:  ' + str(PLAYER_DATA['stats']['HP']),
                 1: 'ATTACK:  ' + str(PLAYER_DATA['stats']['AT']),
                 2: 'DEFENSE:  ' + str(PLAYER_DATA['stats']['DF']),
                 3: 'SPEED:  ' + str(PLAYER_DATA['stats']['SPEED']),
                 4: 'EXP:  ' + str(PLAYER_DATA['stats']['EXP'])}

        if keys[pygame.K_ESCAPE]:
            self.game_instance.stats_menu_open = False
            self.game_instance.player.blocked = not self.game_instance.player.blocked  # So player cant move while mini menu appears again

        self.index = self.index % len(self.items)

    def display_list(self):

        bg_rect = pygame.FRect(self.main_rect.topleft, (self.list_width, self.main_rect.height))
        pygame.draw.rect(self.display_surface, (75, 75, 75), bg_rect)

        v_offset = 0 if self.index < self.rows else -(self.index - self.rows + 1) * self.item_height
        for index, item in self.items.items():

            text_color = 'White'

            top = self.main_rect.top + index * self.item_height + v_offset  # depending on index, the top will be lower and lower
            item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

            text_surf = self.fonts['regular2'].render(item, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(45, 0))

            if item_rect.colliderect(self.main_rect):
                self.display_surface.blit(text_surf, text_rect)

        # lines
        for i in range(min(self.rows, len(self.items))):
            y = self.main_rect.top + self.item_height * i
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, 'black', (left, y), (right, y))

        # shadow
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top))

    def update(self):
        self.input()
        self.display_surface.blit(self.tint_surf, (0, 0))
        self.display_list()
