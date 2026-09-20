import pygame
import button_old
# importing statements

pygame.init()  # must be done for pygame to be initialised

# Variables for screen, frames per second
SCREEN_WIDTH = 800  # Set the screen width variable to 800
SCREEN_HEIGHT = 600  # Set the screen height variable to 600
FPS = 60  # Set the frames per second to 60 which will be important for the game loop when the actual game is created
clock = pygame.time.Clock()  # this will link to the FPS

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # defining screen / display surface with height and
# width defined earlier in a tuple as the arguments
pygame.display.set_caption("Eldritch Echoes")  # setting the caption as Eldritch Echoes as I mentioned in design

# State of screen, random fonts and text colours
state = "initialMenu" # Defining state of the screen
font = pygame.font.SysFont("arialblack", 45)  # Defining font and its size
TEXT_COL = "Black"  # Defining colour in a text colour variable
user_font = pygame.font.SysFont("Callibri", 32)  # Font of users text inputs
font2 = pygame.font.SysFont("arialblack", 80)  # 2nd font defined
font3 = pygame.font.SysFont("Callibri", 55)  # 3rd font defined

# Entry Box Universal Variables
borderColor_active = pygame.Color((207, 206, 204))  # Define colour for active entry box (RGB)
borderColor_passive = pygame.Color("White")  # Define colour for inactive entry box (In text)
userBorderColor = borderColor_passive  # Defining the colour of all boreders to be initially passive
passBorderColor = borderColor_passive
confirmedPassBorderColor = borderColor_passive

# Registration Entry Boxes
username_input_rect = pygame.Rect(80, 245, 140, 32)  # Defining rectangle for username
username_active = False  # Border activation initially set to false
user_text = ""  # Username inputted text from user

password_input_rect = pygame.Rect(80, 370, 140, 32)  # Defining rectangle for password
password_active = False  # Border activation initially set to false
pass_text = ""  # Password inputted text from user

confirmedPassword_input_rect = pygame.Rect(80, 495, 140, 32)  # Defining rectangle for confirmation
confirmedPassword_active = False  # Border activation initially set to false
confirmedPassword_text = ""  # Confirmed password inputted text from user

# load button images
register_img = pygame.image.load("registerButton.png").convert_alpha()  # Use convert alpha for smooth conversion
login_img = pygame.image.load("loginButton.png").convert_alpha()  # Creating the images within variables to use
quit_img = pygame.image.load("quitButton.png").convert_alpha()  # in the arguments for the button class

# button instances
register_button = button.Button(140, 300, register_img, 0.75)  # creating the instances which specify
login_button = button.Button(318, 300, login_img, 0.75)  # the attributes of the buttons
quit_button = button.Button(0, 0, quit_img, 0.75)  # these will not actually draw on the screen straight away
quit_button.rect.topright = (660, 300)  # specified rectangle for quit buttons coordinates on the top right instead

# Draw text on screen
def draw_text(text, font, text_col, x, y):  # defining a draw function with parameters required for text to be drawn
    img = font.render(text, True, text_col)  # Will create img variable as the font rendering the text in certain colour
    screen.blit(img, (x, y))  # drawing img variable ('the text') on the screen display surface mentioned earlier in
    # coordinates x and y specified by user

# game loop
run = True  # defining run variable as True for main game loop

while run:  # while loop for the game loop

    screen.fill((90, 157, 157))  # filling screen with colour specified in tuple with RGB

    if state == "initialMenu":  # Check for the state of the initial menu being true
        draw_text("Welcome To Eldritch Echoes", font, TEXT_COL, 60, 65)  # Use draw text function with arguments
        if register_button.draw(screen):  # Drawing button to screen surface while checking for condition
            state = "registry"  # If true state will change to registry
        if login_button.draw(screen):
            sate = "login"  # If true state will change to login
        if quit_button.draw(screen):
            run = False  # Stopping the game loop for safe exit
            pygame.quit()  # Quitting pygame

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # R E G I S T R Y

    if state == "registry":  # Check if state is equal to 'registry'
        draw_text("Sign Up", font2, TEXT_COL, 80, 45)  # draw text with function
        draw_text("Username", font3, TEXT_COL, 80, 175)
        draw_text("Password", font3, TEXT_COL, 80, 300)
        draw_text("Confirm Password", font3, TEXT_COL, 80, 425)

        usertext_surface = user_font.render(user_text, True, TEXT_COL)  # Define text surface to be drawn to screen for username

        passtext_surface = user_font.render(pass_text, True, TEXT_COL)  # Define text surface to be drawn to screen for password

        cpasstext_surface = user_font.render(confirmedPassword_text, True, TEXT_COL)  # Define text surface to be drawn to screen for the confirmed password

        # Entry Box for USERNAME
        pygame.draw.rect(screen, userBorderColor, username_input_rect)  # Draw the username input rectangle to the screen
        screen.blit(usertext_surface, (username_input_rect.x + 5, username_input_rect.y + 5))  # draw to screen the username text surface at rectangle coordinates
        username_input_rect.w = max(300, usertext_surface.get_width() + 10)  # Allow width of rectangle entry box to stretch
        if username_input_rect.w == 540:  # Make a maximum width for rectangle
            username_input_rect.w = 540

        #  Entry Box for Password
        pygame.draw.rect(screen, passBorderColor, password_input_rect)  # Draw the password input rectangle to the screen
        screen.blit(passtext_surface, (password_input_rect.x + 5, password_input_rect.y + 5))  # draw to screen the password text surface at rectangle coordinates
        password_input_rect.w = max(300, passtext_surface.get_width() + 10)  # Allow width of rectangle entry box to stretch
        if password_input_rect.w == 540:  # Make a maximum width for rectangle
            password_input_rect.w = 540

        # Entry Box for Confirmed Password
        pygame.draw.rect(screen, confirmedPassBorderColor, confirmedPassword_input_rect)  # Draw the confirmation password input rectangle to the screen
        screen.blit(cpasstext_surface, (confirmedPassword_input_rect.x + 5, confirmedPassword_input_rect.y + 5))  # draw cpass text surface at rectangle coordinates
        confirmedPassword_input_rect.w = max(300, cpasstext_surface.get_width() + 10)  # Allow width of rectangle entry box to stretch
        if confirmedPassword_input_rect.w == 540:  # Make a maximum width for rectangle
            confirmedPassword_input_rect.w = 540

        if username_active:  # Checks username active is True
            userBorderColor = borderColor_active  # Sets it to active border colour
        if username_active is False:  # Checks if username active is False
            userBorderColor = borderColor_passive  # Sets it to passive border colour
        if password_active:
            passBorderColor = borderColor_active
        if password_active is False:
            passBorderColor = borderColor_passive
        if confirmedPassword_active:
            confirmedPassBorderColor = borderColor_active
        if confirmedPassword_active is False:
            confirmedPassBorderColor = borderColor_passive


    # Event handler

    for event in pygame.event.get():  # Handles all events in pygame collected using for loop
        if event.type == pygame.QUIT:  # specifies type if type of event is pygame.QUIT
            run = False  # will then end the game loop by setting run as False
            pygame.quit()  # Then will quit safely due to loop being stopped first

        if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for event that indicates user clicks with mouse
            if username_input_rect.collidepoint(event.pos):  # checks its colliding with the user input rect
                username_active = True  # if so username active is set to True
            else:
                username_active = False  # Otherwise it remains False
            if password_input_rect.collidepoint(event.pos):
                password_active = True
            else:
                password_active = False
            if confirmedPassword_input_rect.collidepoint(event.pos):
                confirmedPassword_active = True
            else:
                confirmedPassword_active = False

    pygame.display.update()  # continuously updates the surfaces on the display surface etc as the loop is active