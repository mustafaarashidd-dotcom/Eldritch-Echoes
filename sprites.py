from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = surf.get_frect(topleft=pos)  # floating point rectangle (required for pygame-ce; stores points as
                                                 # not only integers but floating points for greater accuracy)
        self.z = z
        self.y_sort = self.rect.centery - 5
        self.hitbox = self.rect.inflate(0, -15)

class TransitionSprite(Sprite):
    def __init__(self, pos, size, target, groups):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.target = target

class CollidableSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(0, -(self.rect.height * 0.6))

class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, monster, monster_level):
        # data
        self.monster_name = monster
        self.monster_level = monster_level
        self.frames = frames

        # sprite setup
        super().__init__(groups)
        self.image = self.frames
        self.rect = self.image.get_frect(center=pos)

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, pos, bar_pos, frames, groups, player_stats, player_max_stats, font):
        # data
        self.display_surface = pygame.display.get_surface()
        self.player_stats = player_stats
        self.player_max_stats = player_max_stats
        self.font = font
        self.frames = frames
        self.bar_pos = bar_pos

        # current stats
        self.HP = self.player_stats['HP']
        self.AT = self.player_stats['AT']
        self.DF = self.player_stats['DF']
        self.SPEED = self.player_stats['SPEED']
        self.EXP = self.player_stats['EXP']

        # max stats
        self.MAX_HP = self.player_max_stats['HP']

        # health bar
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        text_surf = self.font.render("HEALTH:  ", False, 'white')
        text_rect = text_surf.get_frect(topleft=(self.bar_pos[0]-70, self.bar_pos[1]))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, 'red', (bar_pos[0], bar_pos[1], BAR_WIDTH, BAR_HEIGHT))
        filled_bar_width = int((self.HP / self.MAX_HP) * BAR_WIDTH)
        pygame.draw.rect(self.display_surface, 'green', (self.bar_pos[0], self.bar_pos[1], filled_bar_width, BAR_HEIGHT))

        # sprite setup
        super().__init__(groups)
        self.image = self.frames
        self.rect = self.image.get_frect(center=pos)

        # hitbox
        self.hitbox = self.rect.inflate(-6, -6)

class MonsterNameSprite:
    def __init__(self, text_pos, monster_sprite, font):
        self.display_surface = pygame.display.get_surface()

        text_surf = font.render("NAME:  "+monster_sprite.monster_name.upper(), False, 'white')
        self.text_rect = text_surf.get_frect(topleft=text_pos)
        self.display_surface.blit(text_surf, self.text_rect)
        level_surf = font.render("LEVEL:  "+str(monster_sprite.monster_level).upper(), False, 'white')
        level_pos = (self.text_rect.right+50, text_pos[1])
        self.level_rect = level_surf.get_frect(topleft=level_pos)
        self.display_surface.blit(level_surf, self.level_rect)

class PlayerStatsSprite:
    def __init__(self, pos, monster_sprite, size, groups, font):
        self.monster_sprite = monster_sprite
        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(midbottom=pos)
        self.font = font

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frame_index, self.frames = 0, frames
        super().__init__(pos, frames[self.frame_index], groups, z)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)

class AttackSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups, BATTLE_LAYERS['overlay'])
        self.rect.center = pos

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

    def update(self, dt):
        self.animate(dt)
