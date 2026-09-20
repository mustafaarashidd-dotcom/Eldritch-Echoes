from dialog import DialogTree
from settings import *
from AccountDatabase import *
from game_data import MONSTER_DATA, PLAYER_DATA, ENEMY_DATA

class Entity(pygame.sprite.Sprite):  # Entity shares attributes for both character and player including things like hitbox
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.z = WORLD_LAYERS['main']

        # sprite setup
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(-6, -15)

        self.blocked = False

        self.y_sort = self.rect.centery

    def block(self):  # This is for blocking the players input when the dialog is active
        self.blocked = True
        self.direction = vector(0, 0)

    def unblock(self):  # This is to unblock for when the dialogs have ran out from a character (dialogs in game data)
        self.blocked = False

class Character(Entity):  # make character inherit entities attributes
    def __init__(self, pos, surface, groups, character_data, accountDetails, game_instance):
        super().__init__(pos, surface, groups)
        self.character_data = character_data  # get the character data thats added as an argument when character is called
        self.accountDetails = accountDetails
        self.game_instance = game_instance
        self.flag = False

    def get_dialog(self):  # the get the dialog from the character
        #return self.character_data['dialog'][f'''{'defeated' if self.character_data['defeated'] else 'default'}''']
        # ^^^ return the character data (which is the dictionary) then dialog then the defeated bit
        if self.character_data['position'] == 'island_1':
            change_checkpoint(self.accountDetails[0], 1)
            change_HP(self.accountDetails[0], PLAYER_DATA['stats']['HP'])
            change_AT(self.accountDetails[0], PLAYER_DATA['stats']['AT'])
            change_DF(self.accountDetails[0], PLAYER_DATA['stats']['DF'])
            change_SPEED(self.accountDetails[0], PLAYER_DATA['stats']['SPEED'])
            change_EXP(self.accountDetails[0], PLAYER_DATA['stats']['EXP'])
            change_gold(self.accountDetails[0], self.game_instance.gold)
            change_damage(self.accountDetails[0], self.game_instance.damage)
            save_data_1(ENEMY_DATA['b1']['looted_barrel'], ENEMY_DATA['b2']['looted_barrel'], ENEMY_DATA['c1']['looted_chest'],
                        ENEMY_DATA['m1']['complete'], ENEMY_DATA['o1']['defeated'], ENEMY_DATA['o2']['defeated'],
                        ENEMY_DATA['o1']['killed'], ENEMY_DATA['o2']['killed'], ENEMY_DATA['o1']['spared'], ENEMY_DATA['o2']['spared'],
                        self.accountDetails[0])
        if self.character_data['position'] == 'island_2':
            change_checkpoint(self.accountDetails[0], 2)
            change_HP(self.accountDetails[0], PLAYER_DATA['stats']['HP'])
            change_AT(self.accountDetails[0], PLAYER_DATA['stats']['AT'])
            change_DF(self.accountDetails[0], PLAYER_DATA['stats']['DF'])
            change_SPEED(self.accountDetails[0], PLAYER_DATA['stats']['SPEED'])
            change_EXP(self.accountDetails[0], PLAYER_DATA['stats']['EXP'])
            change_gold(self.accountDetails[0], self.game_instance.gold)
            change_damage(self.accountDetails[0], self.game_instance.damage)
            save_data_2(ENEMY_DATA['b1']['looted_barrel'], ENEMY_DATA['b2']['looted_barrel'], ENEMY_DATA['c1']['looted_chest'],
                        ENEMY_DATA['c2']['looted_chest'], ENEMY_DATA['m1']['complete'], ENEMY_DATA['m2']['complete'],
                        ENEMY_DATA['o1']['defeated'], ENEMY_DATA['o2']['defeated'], ENEMY_DATA['o3']['defeated'],
                        ENEMY_DATA['o1']['killed'], ENEMY_DATA['o2']['killed'], ENEMY_DATA['o3']['killed'], ENEMY_DATA['o1']['spared'],
                        ENEMY_DATA['o2']['spared'], ENEMY_DATA['o3']['spared'], self.accountDetails[0])
        if self.character_data['position'] == 'island_3':
            change_checkpoint(self.accountDetails[0], 3)
            change_HP(self.accountDetails[0], PLAYER_DATA['stats']['HP'])
            change_AT(self.accountDetails[0], PLAYER_DATA['stats']['AT'])
            change_DF(self.accountDetails[0], PLAYER_DATA['stats']['DF'])
            change_SPEED(self.accountDetails[0], PLAYER_DATA['stats']['SPEED'])
            change_EXP(self.accountDetails[0], PLAYER_DATA['stats']['EXP'])
            change_gold(self.accountDetails[0], self.game_instance.gold)
            change_damage(self.accountDetails[0], self.game_instance.damage)
            save_data_3(ENEMY_DATA['b1']['looted_barrel'], ENEMY_DATA['b2']['looted_barrel'], ENEMY_DATA['b3']['looted_barrel'],
                        ENEMY_DATA['b4']['looted_barrel'], ENEMY_DATA['b5']['looted_barrel'], ENEMY_DATA['b6']['looted_barrel'],
                        ENEMY_DATA['c1']['looted_chest'], ENEMY_DATA['c2']['looted_chest'], ENEMY_DATA['c3']['looted_chest'],
                        ENEMY_DATA['c4']['looted_chest'], ENEMY_DATA['c5']['looted_chest'], ENEMY_DATA['c6']['looted_chest'],
                        ENEMY_DATA['m1']['complete'], ENEMY_DATA['m2']['complete'], ENEMY_DATA['m3']['complete'],
                        ENEMY_DATA['o1']['defeated'], ENEMY_DATA['o2']['defeated'], ENEMY_DATA['o3']['defeated'],
                        ENEMY_DATA['o4']['defeated'], ENEMY_DATA['o1']['killed'], ENEMY_DATA['o2']['killed'],
                        ENEMY_DATA['o3']['killed'], ENEMY_DATA['o4']['killed'], ENEMY_DATA['o1']['spared'], ENEMY_DATA['o2']['spared'],
                        ENEMY_DATA['o3']['spared'], ENEMY_DATA['o4']['spared'], self.accountDetails[0])
        if self.character_data['position'] == 'island_4':
            change_checkpoint(self.accountDetails[0], 4)
            change_HP(self.accountDetails[0], PLAYER_DATA['stats']['HP'])
            change_AT(self.accountDetails[0], PLAYER_DATA['stats']['AT'])
            change_DF(self.accountDetails[0], PLAYER_DATA['stats']['DF'])
            change_SPEED(self.accountDetails[0], PLAYER_DATA['stats']['SPEED'])
            change_EXP(self.accountDetails[0], PLAYER_DATA['stats']['EXP'])
            change_gold(self.accountDetails[0], self.game_instance.gold)
            change_damage(self.accountDetails[0], self.game_instance.damage)
            save_data_4(ENEMY_DATA['b1']['looted_barrel'], ENEMY_DATA['b2']['looted_barrel'], ENEMY_DATA['b3']['looted_barrel'],
                        ENEMY_DATA['b4']['looted_barrel'], ENEMY_DATA['b5']['looted_barrel'], ENEMY_DATA['b6']['looted_barrel'],
                        ENEMY_DATA['c1']['looted_chest'], ENEMY_DATA['c2']['looted_chest'], ENEMY_DATA['c3']['looted_chest'],
                        ENEMY_DATA['c4']['looted_chest'], ENEMY_DATA['c5']['looted_chest'], ENEMY_DATA['c6']['looted_chest'],
                        ENEMY_DATA['c7']['looted_chest'], ENEMY_DATA['m1']['complete'], ENEMY_DATA['m2']['complete'],
                        ENEMY_DATA['m3']['complete'], ENEMY_DATA['m4']['complete'], ENEMY_DATA['o1']['defeated'],
                        ENEMY_DATA['o2']['defeated'], ENEMY_DATA['o3']['defeated'], ENEMY_DATA['o4']['defeated'],
                        ENEMY_DATA['o5']['defeated'], ENEMY_DATA['o1']['killed'], ENEMY_DATA['o2']['killed'],
                        ENEMY_DATA['o3']['killed'], ENEMY_DATA['o4']['killed'], ENEMY_DATA['o5']['killed'], ENEMY_DATA['o1']['spared'],
                        ENEMY_DATA['o2']['spared'], ENEMY_DATA['o3']['spared'], ENEMY_DATA['o4']['spared'], ENEMY_DATA['o5']['spared'],
                        self.accountDetails[0])

        if self.character_data['looted_barrel']:
            return self.character_data['dialog']['already_looted']
        elif self.character_data['looted_barrel'] is False:
            self.game_instance.gold += self.character_data['gold']
            self.character_data['looted_barrel'] = True
            return self.character_data['dialog']['default']

        if self.character_data['looted_chest']:
            return self.character_data['dialog']['already_looted']
        elif self.character_data['looted_chest'] is False:
            self.flag = True

        if self.character_data['defeated'] and self.character_data['spared'] and ENEMY_DATA['o5']['pacifist']:
            return self.character_data['dialog']['pacifist_defeat']
        elif self.character_data['defeated'] and (self.character_data['spared'] or self.character_data['killed']) and ENEMY_DATA['o5']['neutral']:
            return self.character_data['dialog']['neutral_defeat']
        elif self.character_data['defeated'] and self.character_data['killed'] and ENEMY_DATA['o5']['genocide']:
            return self.character_data['dialog']['genocide_defeat']
        elif self.character_data['defeated'] and self.character_data['spared']:
            return self.character_data['dialog']['defeated_spared']
        elif self.character_data['complete']:
            return self.character_data['dialog']['complete']
        else:
            return self.character_data['dialog']['default']

class Player(Entity):  # make player inherit entities attributes
    def __init__(self, pos, surf, groups, collision_sprites):
        super().__init__(pos, surf, groups)
        self.image = pygame.Surface((100, 100))
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

        self.direction = vector()

        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            input_vector.y += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1
        self.direction = input_vector

    def move(self, dt):  # parameter is delta time
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * 200 * dt
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')

        self.rect.centery += self.direction.y * 200 * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')

    def collisions(self, axis):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def update(self, dt):  # parameter is delta time
        self.y_sort = self.rect.centery
        if not self.blocked:
            self.input()
            self.move(dt)  # pass dt as argument for move method
