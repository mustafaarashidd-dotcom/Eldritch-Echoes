import pygame
from settings_old import *

class Player(pygame.sprite.Sprite):  # inherit pygame spite class
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)  # initiates the sprite class
        self.image = pygame.image.load("Player_img.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # change hitbox

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {'health': 100, 'attack': 5, 'defense': 0}  # dictionary of stats default
        self.health = self.stats['health']  # set players actual health to default health stat
        self.exp = 0  # set exp to 2, so that we have a testing number to work with


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        # ^^^ this method will be used in a lot of other classes for enemies as well, so for smooth inheritence the
        # speed cannot be self.speed, so I've added it as an argument instead
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed  # split the original statement into x speed and y speed
        self.collision('horizontal')  # check for collisions for each component
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center  # set rectangle center to the new center which is hitbox

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)
