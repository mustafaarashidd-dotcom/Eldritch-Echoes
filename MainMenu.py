import pygame

wave_img = pygame.image.load("waves.png")  # Load wave image


class MainMenuGui:
    def __init__(self, x, y, image, scale):
        width = image.get_width()  # Gathering width integer of image given as argument by the user
        height = image.get_height()  # Gathering height integer of image given as argument by the user
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))  # transforming scale to
        # any possibly required scale that user enters in as argument
        self.rect = self.image.get_rect()  # defining rect variable containing image AS a rectangle (creates borders)
        self.rect.topleft = (x, y)  # Defining x and y coordinates user specifies as argument to shift the top left of

    def draw(self, surface):  # Defining the method of the class that can be used 'draw' with parameter 'surface'

        surface.blit(self.image, (self.rect.x, self.rect.y))  # uses blit function to draw on specifically the surface
