import pygame.transform

from settings import *
from game_data import MONSTER_DATA

class MonsterIndex:
    def __init__(self, monsters, fonts, monster_frames):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.monsters = monsters

        # frames
        self.icon_frames = monster_frames['icons']

        # tint surf
        self.tint_surf = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.tint_surf.set_alpha(200)

        # dimensions
        self.main_rect = pygame.FRect(0, 0, GAME_SCREEN_WIDTH * 0.6, GAME_SCREEN_HEIGHT * 0.8).move_to(center=(GAME_SCREEN_WIDTH / 2, GAME_SCREEN_HEIGHT / 2))

        # list
        self.visible_items = 3
        self.list_width = self.main_rect.width * 0.3
        self.item_height = self.main_rect.height / self.visible_items
        self.index = 0
        self.selected_index = None

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.index -= 1
        if keys[pygame.K_DOWN]:
            self.index += 1
        if keys[pygame.K_SPACE]:
            if self.selected_index != None:
                selected_monster = self.monsters[self.selected_index]
                current_monster = self.monsters[self.index]
                self.monsters[self.index] = selected_monster
                self.monsters[self.selected_index] = current_monster
                self.selected_index = None
            else:
                self.selected_index = self.index

        self.index = self.index % len(self.monsters)

    def display_list(self):
        bg_rect = pygame.FRect(self.main_rect.topleft, (self.list_width, self.main_rect.height))
        pygame.draw.rect(self.display_surface, (75, 75, 75), bg_rect)

        v_offset = 0 if self.index < self.visible_items else -(self.index - self.visible_items + 1) * self.item_height
        for index, monster in self.monsters.items():
            # colors
            if self.index != index:
                bg_color = (75, 75, 75)
            else:
                bg_color = 'light gray'
                #    bg_color = 'light'

            text_color = 'white' if self.selected_index != index else 'gold'

            top = self.main_rect.top + index * self.item_height + v_offset  # depending on index, the top will be lower and lower
            item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

            text_surf = self.fonts['regular'].render(monster.name, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(45, 0))

            icon_surf = self.icon_frames[monster.name]
            icon_rect = icon_surf.get_frect(center=item_rect.midleft + vector(22.5, 0))

            if item_rect.colliderect(self.main_rect):
                # check corners
                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 12)
                elif item_rect.collidepoint(self.main_rect.bottomleft + vector(1, -1)):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 0, 0, 12, 0)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)

                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)

        # lines
        for i in range(min(self.visible_items, len(self.monsters))):
            y = self.main_rect.top + self.item_height * i
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, 'black', (left, y), (right, y))

        # shadow
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top))

    def display_main(self, dt):
        # data
        monster = self.monsters[self.index]

        # main bg
        rect = pygame.FRect(self.main_rect.left+self.list_width, self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height)
        pygame.draw.rect(self.display_surface, '#DECBB6', rect, 0, 12, 0, 12, 0)

        # monster display
        top_rect = pygame.FRect(rect.topleft, (rect.width, rect.height * 0.4))
        pygame.draw.rect(self.display_surface, '#DECBB6', top_rect, 0, 0, 0, 12)
        monster_surf = self.icon_frames[monster.name]
        monster_surf = pygame.transform.scale2x(monster_surf)
        monster_rect = monster_surf.get_frect(center=top_rect.midbottom)
        self.display_surface.blit(monster_surf, monster_rect)

        # text for wanted posters
        wanted_surf = self.fonts['bold2'].render('WANTED', False, 'black')
        name_surf = self.fonts['bold'].render('Name: '+monster.name, False, 'black')
        bounty_surf = self.fonts['bold'].render('Bounty(EXP): '+str(MONSTER_DATA[monster.name]['stats']['EXP']), False, 'black')
        HP_surf = self.fonts['bold'].render('Health: '+str(MONSTER_DATA[monster.name]['stats']['HP']), False, 'black')
        DF_surf = self.fonts['bold'].render('Defense: '+str(MONSTER_DATA[monster.name]['stats']['DF']), False, 'black')
        AT_surf = self.fonts['bold'].render('Attack: '+str(MONSTER_DATA[monster.name]['stats']['AT']), False, 'black')
        SPEED_surf = self.fonts['bold'].render('Speed: '+str(MONSTER_DATA[monster.name]['stats']['SPEED']), False, 'black')

        name_rect = name_surf.get_frect(midleft=rect.midleft+vector(10, 5))
        bounty_rect = bounty_surf.get_frect(topleft=name_rect.bottomleft+vector(0, 30))
        wanted_rect = wanted_surf.get_frect(midbottom=monster_rect.midtop+vector(0, -90))
        HP_rect = HP_surf.get_frect(topleft=bounty_rect.bottomleft+vector(0, 30))
        DF_rect = DF_surf.get_frect(topleft=HP_rect.bottomleft+vector(0, 30))
        AT_rect = AT_surf.get_frect(topleft=DF_rect.bottomleft+vector(0, 30))
        SPEED_rect = SPEED_surf.get_frect(topleft=AT_rect.bottomleft+vector(0, 30))

        self.display_surface.blit(name_surf, name_rect)
        self.display_surface.blit(wanted_surf, wanted_rect)
        self.display_surface.blit(bounty_surf, bounty_rect)
        self.display_surface.blit(HP_surf, HP_rect)
        self.display_surface.blit(DF_surf, DF_rect)
        self.display_surface.blit(AT_surf, AT_rect)
        self.display_surface.blit(SPEED_surf, SPEED_rect)

    def update(self, dt):
        self.input()
        self.display_surface.blit(self.tint_surf, (0, 0))
        self.display_list()
        self.display_main(dt)
        # display the main section