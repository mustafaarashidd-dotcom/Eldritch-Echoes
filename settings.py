import pygame
from pygame.math import Vector2 as vector
from sys import exit

# game setup
GAME_SCREEN_WIDTH = 1280
GAME_SCREEN_HEIGHT = 720
TILE_SIZE = 32
ANIMATION_SPEED = 6

WORLD_LAYERS = {
    'bg': 0,
    'main': 1,
    'top': 2
}

BATTLE_LAYERS = {
    'name': 1,
    'monster': 2,
    'effects': 3,
    'overlay': 4
}
