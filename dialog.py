# imports
from settings import *
from timer import Timer
from game_data import ENEMY_DATA

class DialogTree:  # dialog tree class
    def __init__(self, character, player, all_sprites, font, end_dialog):  # all parameters that are required
        # attributes of the class
        self.player = player
        self.character = character  # player and character needed to test if they are in range
        self.font = font  # font for dialogs
        self.all_sprites = all_sprites  # initialise the all sprites group
        self.end_dialog = end_dialog  # initialise the end dialog method from main code file

        if self.character.character_data['killed'] is not True:
            self.dialog = character.get_dialog()  # set dialog to the characters dialog
            self.dialog_num = len(
                self.dialog)  # dialog number is equal to the length of the dialogs the character has available to use
            self.dialog_index = 0  # dialog index (which dialog from the character) is firstly set to 0

            self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites,
                                               self.font)
            # ^^^ set current dialog to the dialog sprite class below with the dialog index in one of the parameters
            # this will be the dialog that is appearing at all times from the character
        elif self.character.character_data['killed'] and ENEMY_DATA['o5']['genocide']:
            self.dialog = character.get_dialog()  # set dialog to the characters dialog
            self.dialog_num = len(
                self.dialog)  # dialog number is equal to the length of the dialogs the character has available to use
            self.dialog_index = 0  # dialog index (which dialog from the character) is firstly set to 0

            self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites,
                                               self.font)
            # ^^^ set current dialog to the dialog sprite class below with the dialog index in one of the parameters
            # this will be the dialog that is appearing at all times from the character
        elif self.character.character_data['killed'] and ENEMY_DATA['o5']['neutral']:
            self.dialog = character.get_dialog()  # set dialog to the characters dialog
            self.dialog_num = len(
                self.dialog)  # dialog number is equal to the length of the dialogs the character has available to use
            self.dialog_index = 0  # dialog index (which dialog from the character) is firstly set to 0

            self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites,
                                               self.font)
            # ^^^ set current dialog to the dialog sprite class below with the dialog index in one of the parameters
            # this will be the dialog that is appearing at all times from the character
        else:
            self.dialog = "Killed"
            self.dialog_num = 0
            self.dialog_index = 0
            self.current_dialog = DialogSprite(self.dialog, self.character, self.all_sprites, self.font)

        self.dialog_timer = Timer(500, autostart=True)  # start the dialog timer for 0.5 seconds (500 milliseconds)

    def input(self):  # collecting input class
        keys = pygame.key.get_just_pressed()  # get keys
        if keys[pygame.K_SPACE] and not self.dialog_timer.active:  # check if key is space and dialog timer being active isnt true
            self.current_dialog.kill()  # kill the current dialog
            self.dialog_index += 1  # increment the dialog index so the next one would appear
            if self.dialog_index < self.dialog_num:  # if the dialog index is less than the amount of dialogs (dialogs has not ran out yet)
                self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)  # create the current dialog again with the new index
                self.dialog_timer.activate()  # activate timer immediately afterwards so the same thing can happen again form line 25
            else:
                # if dialogs have ran out run the end dialog class from main code file on the character
                if self.character.character_data['enemy'] and self.character.character_data['defeated'] is False:
                    self.end_dialog(self.character)
                    self.character.character_data['in_combat'] = True
                self.end_dialog(self.character)

        if self.character.flag and not self.dialog_timer.active:
            if keys[pygame.K_y]:
                self.current_dialog.kill()
                self.end_dialog(self.character)
                if self.character.game_instance.gold < self.character.character_data['gold']:
                    self.dialog = self.character.character_data['dialog']['decline']
                else:
                    self.character.game_instance.gold -= self.character.character_data['gold']
                    next_key = max(self.character.game_instance.inventory_dict.keys()) + 1 if self.character.game_instance.inventory_dict else 0
                    self.character.game_instance.inventory_dict.update({next_key: self.character.character_data['item']})
                    self.character.character_data['looted_chest'] = True
                    # SAVE PROGRESS HERE BY ADDING TO ACCOUNT DATABASE NEW FIELD
                self.character.flag = False

    def update(self):  # update method
        # initialise the main methods
        self.dialog_timer.update()  # update the dialog timer
        self.input()  # get the input

class DialogSprite(pygame.sprite.Sprite):  # this class is for actually making the dialog on the screen hence the sprite inheritence
    def __init__(self, message, character, groups, font):  # parameters required
        super().__init__(groups)  # initialise the parent class (pygame.sprite.Sprite)
        self.z = WORLD_LAYERS['top']  # make some random variable z which is equivalent to the world layers dict: top, which has the value 2 (in settings)

        # text
        text_surf = font.render(message, False, 'black')  # create the text surface
        padding = 2.5  # create padding around the message
        width = max(15, text_surf.get_width() + padding * 2)  # width should be either 15 or the texts width plus padding times 2, depending on which is larger
        height = text_surf.get_height() + padding * 2  # height should just be text surfaces height plus padding times 2

        # background
        surf = pygame.Surface((width, height), pygame.SRCALPHA)  # create surface, SRCALPHA is to support transparency
        surf.fill((0, 0, 0, 0))  # fill surface with colour being black
        pygame.draw.rect(surf, '#FFFFFF', surf.get_frect(topleft=(0, 0)), 0, 4)  # draw rectangle surface behind the text that will be white (for easier view)
        # may change from white to a colour fitting the theme a bit more later on, still with easier view
        surf.blit(text_surf, text_surf.get_frect(center=(width / 2, height / 2)))  # blit text surface to the screen

        self.image = surf  # image set to surface
        self.rect = self.image.get_frect(midbottom=character.rect.midtop + vector(0, -5))  # make image a rectangle (for background of text dialogs)
