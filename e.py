import pygame
import button_old
import time

pygame.init()

# Variables for screen, frames per second
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eldritch Echoes")

# State of screen, random fonts and text colours
state = "initialMenu"
font = pygame.font.SysFont("arialblack", 45)
font2 = pygame.font.SysFont("arialblack", 80)
font3 = pygame.font.SysFont("Callibri", 55)
font4 = pygame.font.SysFont("arialblack", 20)
TEXT_COL = "Black"
TEXT_COL2 = "lightGrey"
TEXT_COL3 = "Red"
user_font = pygame.font.SysFont("Calibri", 32)  # Font of users text inputs
show_error_message = False
error_message_timestamp = 0

# Entry Box Universal Variables
borderColor_active = pygame.Color((207, 206, 204))
borderColor_passive = pygame.Color("White")
userBorderColor = borderColor_passive
passBorderColor = borderColor_passive
confirmedPassBorderColor = borderColor_passive

# Registration Entry Boxes
username_input_rect = pygame.Rect(80, 245, 140, 32)
username_active = False
user_text = "Enter Username"  # Username inputted text from user

password_input_rect = pygame.Rect(80, 370, 140, 32)
password_active = False
pass_text = "Enter Password"  # Password inputted text from user

confirmedPassword_input_rect = pygame.Rect(80, 495, 140, 32)
confirmedPassword_active = False
confirmedPassword_text = "Enter Password Again"  # Confirmed password inputted text from user

# load button images
register_img = pygame.image.load("registerButton.png").convert_alpha()
login_img = pygame.image.load("loginButton.png").convert_alpha()
quit_img = pygame.image.load("quitButton.png").convert_alpha()
back_img = pygame.image.load("backButton.png").convert_alpha()
delete_img = pygame.image.load("deleteButton.png").convert_alpha()
submit_img = pygame.image.load("submitButton.png").convert_alpha()

# button instances
register_button = button.Button(140, 300, register_img, 0.75)
login_button = button.Button(318, 300, login_img, 0.75)
quit_button = button.Button(0, 0, quit_img, 0.75)
quit_button.rect.topright = (660, 300)
back_button = button.Button(25, 20, back_img, 0.1)
username_delete_button = button.Button(620, 245, delete_img, 0.42)
password_delete_button = button.Button(620, 370, delete_img, 0.42)
confirmedPassword_delete_button = button.Button(620, 495, delete_img, 0.42)
submit_button = button.Button(691, 565, submit_img, 1)

# Draw text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Check for alphabetical and digital characters in a string
def contains_alpha_digits_and_symbols(s):
    has_alpha = any(char.isalpha() for char in s)
    has_digits = any(char.isdigit() for char in s)
    has_symbols = not s.isalnum()
    return has_alpha and has_digits and has_symbols

# game loop
run = True
while run:

    screen.fill((90, 157, 157))

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # I N I T I A L M E N U S C R E E N

    if state == "initialMenu":
        draw_text("Welcome To Eldritch Echoes", font, TEXT_COL, 60, 65)
        if register_button.draw(screen):
            state = "registry"
        if login_button.draw(screen):
            state = "login"
        if quit_button.draw(screen):
            run = False
            pygame.quit()

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # R E G I S T R Y

    if state == "registry":
        draw_text("Sign Up", font2, TEXT_COL, 80, 45)
        draw_text("Username", font3, TEXT_COL, 80, 175)
        draw_text("Password", font3, TEXT_COL, 80, 300)
        draw_text("Confirm Password", font3, TEXT_COL, 80, 425)

        # TODO: Ensure that clicking enter key while text is of no width leads to no error

        if username_active is False and user_text == "":
            user_text = "Enter Username"
        if username_active and user_text == "":
            usertext_surface = None
        if user_text == "Enter Username":
            usertext_surface = user_font.render(user_text, True, TEXT_COL2)
        else:
            usertext_surface = user_font.render(user_text, True, TEXT_COL)

        if pass_text == "Enter Password":
            passtext_surface = user_font.render(pass_text, True, TEXT_COL2)
        else:
            passtext_surface = user_font.render(pass_text, True, TEXT_COL)

        if confirmedPassword_text == "Enter Password Again":
            cpasstext_surface = user_font.render(confirmedPassword_text, True, TEXT_COL2)
        else:
            cpasstext_surface = user_font.render(confirmedPassword_text, True, TEXT_COL)

        # Entry Box for USERNAME
        pygame.draw.rect(screen, userBorderColor, username_input_rect)
        screen.blit(usertext_surface, (username_input_rect.x + 5, username_input_rect.y + 2))
        username_delete_button.rect.midleft = username_input_rect.midright
        username_input_rect.w = max(300, usertext_surface.get_width() + 10)
        if username_input_rect.w == 540:
            username_input_rect.w = 540

        # Entry Box for Password
        pygame.draw.rect(screen, passBorderColor, password_input_rect)
        screen.blit(passtext_surface, (password_input_rect.x + 5, password_input_rect.y + 2))
        password_delete_button.rect.midleft = password_input_rect.midright
        password_input_rect.w = max(300, passtext_surface.get_width() + 10)
        if password_input_rect.w == 540:
            password_input_rect.w = 540

        # Entry Box for Confirmed Password
        pygame.draw.rect(screen, confirmedPassBorderColor, confirmedPassword_input_rect)
        screen.blit(cpasstext_surface, (confirmedPassword_input_rect.x + 5, confirmedPassword_input_rect.y + 2))
        confirmedPassword_delete_button.rect.midleft = confirmedPassword_input_rect.midright
        confirmedPassword_input_rect.w = max(300, cpasstext_surface.get_width() + 10)
        if confirmedPassword_input_rect.w == 540:
            confirmedPassword_input_rect.w = 540

        if back_button.draw(screen):
            state = "initialMenu"
        if username_delete_button.draw(screen) and user_text != "Enter Username":
            user_text = ""
        if password_delete_button.draw(screen) and pass_text != "Enter Password":
            pass_text = ""
        if confirmedPassword_delete_button.draw(screen) and confirmedPassword_text != "Enter Password Again":
            confirmedPassword_text = ""

        if submit_button.draw(screen):
            if len(pass_text) >= 5 and confirmedPassword_text == pass_text and \
                    contains_alpha_digits_and_symbols(pass_text) is True and \
                    contains_alpha_digits_and_symbols(confirmedPassword_text) is True:
                print("SUCCESS!")
            else:
                show_error_message = True
                error_message_timestamp = time.time()

        if show_error_message:
            draw_text("Please fill username, password must contain 1 symbol,", font4, TEXT_COL3, 125, 10)
            draw_text("1 letter and 1 number and must be 5 or more characters long", font4, TEXT_COL3, 125, 35)
            if time.time() - error_message_timestamp >= 10:
                show_error_message = False

        if username_active:
            userBorderColor = borderColor_active
        if username_active is False:
            userBorderColor = borderColor_passive
        if password_active:
            passBorderColor = borderColor_active
        if password_active is False:
            passBorderColor = borderColor_passive
        if confirmedPassword_active:
            confirmedPassBorderColor = borderColor_active
        if confirmedPassword_active is False:
            confirmedPassBorderColor = borderColor_passive

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # L O G I N

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_input_rect.collidepoint(event.pos):
                username_active = True
                if user_text == "Enter Username":
                    user_text = ""
            else:
                username_active = False
            if password_input_rect.collidepoint(event.pos):
                password_active = True
                if pass_text == "Enter Password":
                    pass_text = ""
            else:
                password_active = False
            if confirmedPassword_input_rect.collidepoint(event.pos):
                confirmedPassword_active = True
                if confirmedPassword_text == "Enter Password Again":
                    confirmedPassword_text = ""
            else:
                confirmedPassword_active = False

        if event.type == pygame.KEYDOWN and username_active is True:
            if len(user_text) == 0 and event.key == pygame.K_BACKSPACE:
                pass
            if len(user_text) == 19:
                user_text = user_text
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

        if event.type == pygame.KEYDOWN and password_active is True:
            if len(pass_text) == 0 and event.key == pygame.K_BACKSPACE:
                pass
            if len(pass_text) == 20:
                pass_text = pass_text
            elif event.key == pygame.K_BACKSPACE:
                pass_text = pass_text[:-1]
            else:
                pass_text += event.unicode
            if event.key == pygame.K_RETURN:
                password_active = False

        if event.type == pygame.KEYDOWN and confirmedPassword_active is True:
            if len(confirmedPassword_text) == 0 and event.key == pygame.K_BACKSPACE:
                pass
            if len(confirmedPassword_text) == 20:
                confirmedPassword_text = confirmedPassword_text
            elif event.key == pygame.K_BACKSPACE:
                confirmedPassword_text = confirmedPassword_text[:-1]
            else:
                confirmedPassword_text += event.unicode
            if event.key == pygame.K_RETURN:
                confirmedPassword_active = False

    pygame.display.update()

