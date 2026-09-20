import pygame

# Whenever self is mentioned it is used because it is representing the instance of the class Button
# It will bind the attributes with the given arguments


class Button:  # Defining the class (must always be capitalized)
    def __init__(self, x, y, image, scale):  # Defining, using init method, the attributes of the class
        width = image.get_width()  # Gathering width integer of image given as argument by the user
        height = image.get_height()  # Gathering height integer of image given as argument by the user
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))  # transforming scale to
        # any possibly required scale that user enters in as argument
        self.rect = self.image.get_rect()  # defining rect variable containing image AS a rectangle (creates borders)
        self.rect.topleft = (x, y)  # Defining x and y coordinates user specifies as argument to shift the top left of
        # rectangle, whenever it is moved it should be regarded that the top left of rectangle will move nowhere else
        self.clicked = False  # defining 'clicked' variable as False to scan if user clicks with mouse or not later on

    def draw(self, surface):  # Defining the method of the class that can be used 'draw' with parameter 'surface'
        action = False  # defining variable action as False, will be VERY useful tool in the main code later on
        pos = pygame.mouse.get_pos()  # Taking position of users mouse coordinates as 'pos' <-- identifier

        if self.rect.collidepoint(pos):  # Using collidepoint function to check if the users mouse collides with
            # button rectangle
            self.clicked = True
            for event in pygame.event.get():  # Collects events for when class method is called (should be in main loop)
                if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for mouse button down event (when mouse has just been clicked)
                    self.clicked = True  # If so self.clicked will become True
                    action = True  # Action that will take place will also turn true when mouse is clicked but not held

        if pygame.mouse.get_pressed()[0] == 0:  # checks if its 0, so mouse is not clicked
            self.clicked = False  # will set the clicked variable as False

        surface.blit(self.image, (self.rect.x, self.rect.y))  # uses blit function to draw on specifically the surface
        # defined in argument by the user (for us that will be 'screen', it will draw the image at rectangle coordinates
        # x and y also specified by user which will be the top right of the rectangle.

        return action
        # Will return the boolean value of action (super useful to check if the button has been clicked
        # or not so we can define what will happen after that happens)

class Button2():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, scale):  # Set parameters
        self.scale = scale  # The scale is whats inputted as scale
        self.image = image  # The image is whats inputted as the image
        self.width = image.get_width()  # Gathering width integer of image given as argument by the user
        self.height = image.get_height()  # Gathering height integer of image given as argument by the user
        self.x_pos = pos[0]  # Sets the x position to the first index of position tuple (x, y)
        self.y_pos = pos[1]  # Sets the y position to the second index of the position tuple (x, y)
        self.font = font  # The font is whats inputted as font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text  # If no image is inputted with arguments then image is the text
        else:
            self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))  # transforming scale
            # to any possibly required scale that user enters in as argument if an image is inputted as an argument only
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))  # Set image into rectangle x and y position
        self.text_x_pos = ((self.rect.right-self.rect.left)/2) + self.x_pos  # Define x position for text
        self.text_y_pos = ((self.rect.bottom-self.rect.top)/2) + self.y_pos  # Define y position for text
        self.text_rect = self.text.get_rect(center=(self.text_x_pos, self.text_y_pos))  # Define text rectangle

    def update(self, screen):  # Update method, parameters: screen
        if self.image is not None:  # If the image was inputted
            screen.blit(self.image, self.rect)  # Draw image at rectangle positions (self.rect attribute defined above)
        screen.blit(self.text, self.text_rect)  # Otherwise draw the text in the text rectangle coordinates instead

    def checkForInput(self, position):  # Check for input method, parameters: position
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True  # If position inputted as argument is in range anywhere in the rectangle then return true
        return False  # otherwise return false, there is no collision between mouse position and rectangle

    def changeColor(self, position):  # Change colour method, parameters: position
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)  # If position of argument is in rectangle
            # then set the text equal to the rendered font with text input and hovering colour
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)  # Otherwise ensure the text is the same
            # but make sure when rendered, the colour is base colour
