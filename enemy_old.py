import pygame
from settings_old import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name, pos, groups, surface=pygame.Surface((TILESIZE, TILESIZE))):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.monster_name = monster_name

        # graphics setup
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)

    def check_collisions(self, mouse_position):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1]\
                in range(self.rect.top, self.rect.bottom):
            return True
        return False

        # issue with self.rect.left and the rest of the values in the range function,
        # they seem to give rather than a single number a series of numbers

        # potentially rising issue: for some reason enemy class is being linked with player class a lot
