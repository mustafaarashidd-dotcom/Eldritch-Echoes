import pygame
from settings_old import *
from tile_old import Tile
from player_old import Player
from debug import debug
from support_old import *
from ui_old import UI
from enemy_old import Enemy
#from MainCodeFile import game_mouse_pos

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()  # To sort Y and the camera on the sprites which are visible
        self.obstacle_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        
        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        # dictionaries that are used to draw out the csv for each layer using the graphics for each ID that matches the name of the image in graphics
        layouts = {
            'boundary': import_csv_layout('EldritchEchoesMap_FloorBlocks.csv'),
            'object2': import_csv_layout('EldritchEchoesMap_Objects2.csv'),
            'object': import_csv_layout('EldritchEchoesMap_Objects.csv'),
            'entities': import_csv_layout('EldritchEchoesMap_Entities.csv')
        }
        graphics = {
            'objects2': import_folder('Tiles'),
            'objects': import_folder('Tiles'),
            'entities': import_folder('Tiles')
        }

        for style, layout in layouts.items():  # for instance style is boundary and layout is import csv function
            for row_index, row in enumerate(layout):  # same logic as before
                for col_index, col in enumerate(row):  # same logic as before
                    if col != '-1':  # same logic as before
                        x = col_index * TILESIZE  # same logic as before
                        y = row_index * TILESIZE  # same logic as before
                        #if style == 'boundary':  # check the dictionary style is equal to boundary
                        #    Tile((x, y), [self.obstacle_sprites], 'invisible')  # draw tile for floor blocks
                        if style == 'object2':  # check if style is equal to object2
                            surf = graphics['objects2'][int(col)]  # create surface from the graphics for each column (ID) as an integer
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object2', surf)  # draw object2
                        if style == 'object':  # check if style is equal to object
                            surf = graphics['objects'][int(col)]  # create surface from graphics for each column (ID) as an integer
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)  # draw objects
                        if style == 'entities':
                            if col == '136':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites)  # draw player to screen)
                            else:
                                if col == '124':  # column/ID in the csv file references the specific entity
                                    surf = graphics['entities'][int(col)]
                                    Enemy('mermaid', (x, y), [self.visible_sprites, self.obstacle_sprites], surf)

                                elif col == '103':
                                    surf = graphics['entities'][int(col)]
                                    self.animal = Enemy('animal', (x, y), [self.visible_sprites, self.obstacle_sprites], surf)

                                elif col == '120':
                                    surf = graphics['entities'][int(col)]
                                    Enemy('sharks', (x, y), [self.visible_sprites, self.obstacle_sprites], surf)
                                elif col == '127':
                                    surf = graphics['entities'][int(col)]
                                    Enemy('captain_dreadful', (x, y), [self.visible_sprites, self.obstacle_sprites], surf)
                                elif col == '122':
                                    surf = graphics['entities'][int(col)]
                                    Enemy('spirit', (x, y), [self.visible_sprites, self.obstacle_sprites], surf)
                                elif col == '126':
                                    surf = graphics['entities'][int(col)]
                                    Enemy('captain_marduk', (x, y), [self.visible_sprites, self.obstacle_sprites], surf)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)  # Draw visible sprites to the screen (display surface)
        # The reason to only do .draw is because the drawn sprites in visible sprite group will be updated
        # constantly to the screen after being ran before the pygame.display.update function in main code file
        self.visible_sprites.update()  # Use update method on the sprites to update screen
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2  # get half width and height
        self.half_height = self.display_surface.get_size()[1] // 2  # of the display surface
        self.offset = pygame.math.Vector2()  # how much camera should move

        # creating the floor
        self.floor_surf = pygame.image.load("EldritchEchoesMap_ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset  # offset the position from the floor (ground of map)
        self.display_surface.blit(self.floor_surf, floor_offset_pos)  # draw floor surface to display surface at the
                                                                      # offset position just created in line 62

        #for sprite in self.sprites():  # for all sprites in our sprite groups
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset  # create offset position of camera
            self.display_surface.blit(sprite.image, offset_pos)  # draw sprites at offset position
