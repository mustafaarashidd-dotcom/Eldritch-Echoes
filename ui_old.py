import pygame
from settings_old import *

class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()  # Collect display surface to draw on
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Create the font

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount  # players current hp divided by the max amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):  # Method to show exp on screen
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)  # Create text surface
        x = self.display_surface.get_size()[0] - 20  # Set x to the display surface size in x and add padding of 20
        y = self.display_surface.get_size()[1] - 20  # Set y to the display surface size in y and add padding of 20
        # padding of 20 so that it's a little distances from the bottom right corner
        text_rect = text_surf.get_rect(bottomright=(x, y))  # set text surface into a text rect to x and y coordinate

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))  # draw text rect
        # inflate function used to make the box around the actual text surface a bit bigger than the text surface
        self.display_surface.blit(text_surf, text_rect)  # draw text surface where text rects x and y coordinates are
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)  # draw text rects border

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.show_exp(player.exp)  # run show exp method with exp argument as the players exp
