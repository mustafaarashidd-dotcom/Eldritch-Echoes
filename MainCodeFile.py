# Importing statements
from button import *
import time
from AccountDatabase import *
import MainMenu
import sys
from settings import *
from pytmx.util_pygame import load_pygame
from support import check_connections, import_folder_dict, audio_importer, attack_importer
from os.path import join

from game_data import *
from dialog import DialogTree

from sprites import Sprite, CollidableSprite, TransitionSprite
from entities import Player, Character
from groups import AllSprites
from monster import Monster
from monster_index import MonsterIndex
from mini_menu import MiniMenu
from mini_menu import Inventory
from mini_menu import Stats_menu
from battle import Battle

# Pygame is imported from other imports like button page

pygame.init()  # must be done for pygame to be initialised

# Music
main_menu_music = pygame.mixer.Sound("audio/main.ogg")  # Define the music file
mainMenu_music_playing = False  # Ensure that music playing is false, so we can play music once in main loop

# Variables for screen, frames per second
SCREEN_WIDTH = 800  # Set the screen width variable to 800
SCREEN_HEIGHT = 600  # Set the screen height variable to 600
FPS = 60  # Set the frames per second to 60 which will be important for the game loop when the actual game is created
clock = pygame.time.Clock()  # this will link to the FPS

# Time Based Messages
registerSuccessMessage_timestamp = 0  # Time stamp for the success message during submit process when registering
registerErrorMessage_timestamp = 0  # Time stamp for error message during submit process when registering
show_registerError_message = False  # Error message not to be shown initially
show_registerSuccess_message = False  # Account registered message not to be shown initially
loginErrorMessage_timestamp = 0  # For login page
show_loginError_message = False  # For login page

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # defining screen / display surface with height and
# width defined earlier in a tuple as the arguments
pygame.display.set_caption("Eldritch Echoes")  # setting the caption as Eldritch Echoes as I mentioned in design
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# State of screen, random fonts and text colours
state = "initialMenu"  # Defining state of the screen
font = pygame.font.SysFont("arialblack", 45)  # Defining font and its size
TEXT_COL = "Black"  # Defining colour in a text colour variable
user_font = pygame.font.SysFont("Calibri", 32)  # Font of users text inputs
font2 = pygame.font.SysFont("arialblack", 80)  # 2nd font defined
font3 = pygame.font.SysFont("Calibri", 55)  # 3rd font defined
TEXT_COL2 = "lightGrey"
font4 = pygame.font.SysFont("arialblack", 20)
TEXT_COL3 = "Red"
TEXT_COL4 = "Green"
font5 = pygame.font.SysFont("arialblack", 90)
font6 = pygame.font.SysFont(None, 165)
TEXT_COL5 = (86, 208, 216)
font7 = pygame.font.SysFont("arialblack", 30)
font8 = pygame.font.Font(join('PixeloidSans.ttf'), 25)

# Entry Box Universal Variables
borderColor_active = pygame.Color((207, 206, 204))  # Define colour for active entry box (RGB)
borderColor_passive = pygame.Color("White")  # Define colour for inactive entry box (In text)
userBorderColor = borderColor_passive  # Defining the colour of all borders to be initially passive
passBorderColor = borderColor_passive
confirmedPassBorderColor = borderColor_passive
loginUserBorderColor = borderColor_passive  # Specifically for the login
loginPassBorderColor = borderColor_passive  # Specifically for the login

# Registration Entry Boxes
username_input_rect = pygame.Rect(80, 245, 140, 32)  # Defining rectangle for username
username_active = False  # Border activation initially set to false
user_text = "Enter Username"  # Username inputted text from user

password_input_rect = pygame.Rect(80, 370, 140, 32)  # Defining rectangle for password
password_active = False  # Border activation initially set to false
pass_text = ""  # Password inputted text from user
displayed_pass_text = "Enter Password"

confirmedPassword_input_rect = pygame.Rect(80, 495, 140, 32)  # Defining rectangle for confirmation
confirmedPassword_active = False  # Border activation initially set to false
confirmedPassword_text = ""  # Confirmed password inputted text from user
displayed_confirmedPassword_text = "Enter Password Again"

# Login Entry Boxes
loginUsername_input_rect = pygame.Rect(80, 295, 140, 32)  # Specifically for the login page
loginUsername_active = False  # Specifically for the login page
loginUser_text = "Enter Username"  # Specifically for login page

loginPassword_input_rect = pygame.Rect(80, 455, 140, 32)  # Specifically for the login page
loginPassword_active = False  # Specifically for the login page
loginPass_text = ""  # Specifically for login page
loginDisplayed_pass_text = "Enter Password"  # Specifically for login page

# load button images
delete_img = pygame.image.load("deleteButton.png").convert_alpha()  # Load button image for delete button
submit_img = pygame.image.load("submitButton.png").convert_alpha()  # Load button image for submit button
back_img = pygame.image.load("backButton.png").convert_alpha()  # Load button image for back button

# Database Management
def user_validating(user_text):  # Create function with user text as parameter
    conn = sqlite3.connect("EldritchEchoesAccounts.db")
    c = conn.cursor()

    # Fetch the list of usernames from the database again (refreshes list)
    c.execute("SELECT username FROM AccountInfo")  # Select username field from account information
    usernames = c.fetchall()  # Fetch all the usernames and place them within a variable called usernames
    conn.commit()

    found = False  # Setup found variable as False
    for tup in usernames:  # Run through all tuples in the list
        for users in tup:  # Run through all data items in the tuple (usernames) and set this as 'users'
            if user_text == users:  # compare user text with users
                found = True  # If they're identical set found to true
                break
    conn.close()
    return found  # Return value of found, whether its true or false

def login_validating(username, password):
    conn = sqlite3.connect("EldritchEchoesAccounts.db")  # Same database set up logic
    c = conn.cursor()

    c.execute("SELECT username, password FROM AccountInfo")  # SQL statement returns all values of username and password
    records = c.fetchall()  # all records
    conn.commit()
    login_record = (username, password)  # Local variable (only needed temporarily for comparison validation)

    found = False
    for i in records:
        if login_record == i:  # Checks if the record is identical to any in the database table
            found = True

    conn.close()
    return found  # Remember if found is true then login is successful otherwise its a fail

# Draw text on screen
def draw_text(text, font, text_col, x, y):  # defining a draw function with parameters required for text to be drawn
    img = font.render(text, True, text_col)  # Will create img variable as the font rendering the text in certain colour
    screen.blit(img, (x, y))  # drawing img variable ('the text') on the screen display surface mentioned earlier in
    # coordinates x and y specified by user

def get_font(size):
    font = pygame.font.SysFont("arialblack", size)
    return font

# Check for alphabetical and digital characters in a string
def contains_alpha_digits_and_symbols(text):  # defining the checking contains alphabet, digits and symbols function
    has_alpha = any(char.isalpha() for char in text)  # has alpha variable equal to any characters that are alphabetical
    has_digits = any(char.isdigit() for char in text)  # has digits symbol equals any character that is a number
    has_symbols = not text.isalnum()  # has symbols equals text not being only numbers and letters (alphanumerical).
    return has_alpha and has_digits and has_symbols  # return if either variable is true or false

# Screens
def initial_menu():
    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # defining screen / display surface with height and width
    while True:
        screen.fill((90, 157, 157))  # Fill screen with colour
        InitialMenu_mouse_pos = pygame.mouse.get_pos()  # Collect mouse coordinates
        draw_text("Welcome To Eldritch Echoes", font, TEXT_COL, 60, 65)  # Draw text for initial menu

        # Create button instances with the second button class
        REGISTER_BUTTON = Button2(image=pygame.image.load("InitialMenuButtonRects.png"), pos=(75, 325),
                                     text_input="REGISTER", font=font7, base_color="Black",
                                     hovering_color="Grey", scale=1)
        LOGIN_BUTTON = Button2(image=pygame.image.load("InitialMenuButtonRects.png"), pos=(316, 325),
                                     text_input="LOGIN", font=font7, base_color="Black",
                                     hovering_color="Grey", scale=1)
        QUIT_BUTTON = Button2(image=pygame.image.load("InitialMenuButtonRects.png"), pos=(555, 325),
                                     text_input="QUIT", font=font7, base_color="Black",
                                     hovering_color="Grey", scale=1)

        # Renders all button instances so that the change colour method has been issues with the mouse coordinates and
        # the buttons have been drawn to the screen (aka the display surface)
        for button in [QUIT_BUTTON, LOGIN_BUTTON, REGISTER_BUTTON]:
            button.changeColor(InitialMenu_mouse_pos)
            button.update(screen)

        # Seperate event handler for each component that also handles button clicks in its own event handler
        # Making it more compatible with the 2nd button class so we can use the mouse button down condition instead
        # of the other one, this will lead to less crashes and glitches in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks event is mouse button down and is left click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Checks for input with buttons
                if QUIT_BUTTON.checkForInput(InitialMenu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if LOGIN_BUTTON.checkForInput(InitialMenu_mouse_pos):
                    login()
                if REGISTER_BUTTON.checkForInput(InitialMenu_mouse_pos):
                    register()

        pygame.display.update()  # Update the display
        clock.tick(FPS)  # Set the Frames Per Second to 60 (FPS)

def register():
    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # defining screen / display surface with height and width
    while True:
        screen.fill((90, 157, 157)) # Fill screen with colour
        InitialMenu_mouse_pos = pygame.mouse.get_pos()  # Collect mouse coordinates

        # Set variables to global
        global user_text
        global displayed_pass_text
        global displayed_confirmedPassword_text
        global userBorderColor
        global passBorderColor
        global confirmedPassBorderColor
        global confirmedPassword_text
        global pass_text
        global show_registerError_message
        global registerErrorMessage_timestamp
        global show_registerSuccess_message
        global registerSuccessMessage_timestamp
        global username_active
        global password_active
        global confirmedPassword_active
        global mods
        global position

        position = 'island1'

        draw_text("Sign Up", font2, TEXT_COL, 80, 45)  # draw text with function
        draw_text("Username", font3, TEXT_COL, 80, 175)
        draw_text("Password", font3, TEXT_COL, 80, 308)
        draw_text("Confirm Password", font3, TEXT_COL, 80, 442)

        # Username Text Surface
        if user_text == "" and username_active is False:  # Must check that the text is not being entered
            user_text = "Enter Username"  # If its empty nothing + it being entered then it'll set to 'Enter Username'
        if user_text == "Enter Username":
            usertext_surface = user_font.render(user_text, True, TEXT_COL2)
            # ^^^ Define text surface to be drawn to screen for username
        else:
            usertext_surface = user_font.render(user_text, True, TEXT_COL)

        # Password Text Surface
        if displayed_pass_text == "" and password_active is False:  # Similar scenario as above
            displayed_pass_text = "Enter Password"
        if displayed_pass_text == "Enter Password":
            displayedpasstext_surface = user_font.render(displayed_pass_text, True, TEXT_COL2)
        else:
            displayedpasstext_surface = user_font.render(displayed_pass_text, True, TEXT_COL)

        # Confirm Password Text Surface
        if displayed_confirmedPassword_text == "" and confirmedPassword_active is False:  # Same scenarios as the above
            displayed_confirmedPassword_text = "Enter Password Again"
        if displayed_confirmedPassword_text == "Enter Password Again":
            displayedcpasstext_surface = user_font.render(displayed_confirmedPassword_text, True, TEXT_COL2)
        else:
            displayedcpasstext_surface = user_font.render(displayed_confirmedPassword_text, True, TEXT_COL)

        # Entry Box for Username
        pygame.draw.rect(screen, userBorderColor, username_input_rect)
        # ^^^ Draw the username input rectangle to the screen
        screen.blit(usertext_surface, (username_input_rect.x + 5, username_input_rect.y + 2))
        # ^^^ Draw to screen the username text surface at rectangle coordinates
        username_input_rect.w = max(300, usertext_surface.get_width() + 10)
        # ^^^ Allow width of rectangle entry box to stretch
        if username_input_rect.w == 540:  # Make a maximum width for rectangle
            username_input_rect.w = 540

        #  Entry Box for Password
        pygame.draw.rect(screen, passBorderColor, password_input_rect)
        # ^^^ Draw the password input rectangle to the screen
        screen.blit(displayedpasstext_surface, (password_input_rect.x + 5, password_input_rect.y + 2))
        # ^^^ draw to screen the password text surface at rectangle coordinates
        password_input_rect.w = max(300, displayedpasstext_surface.get_width() + 10)
        # ^^^ Allow width of rectangle entry box to stretch
        if password_input_rect.w == 540:  # Make a maximum width for rectangle
            password_input_rect.w = 540

        # Entry Box for Confirmed Password
        pygame.draw.rect(screen, confirmedPassBorderColor, confirmedPassword_input_rect)
        # ^^^ Draw the confirmation password input rectangle to the screen
        screen.blit(displayedcpasstext_surface,
                    (confirmedPassword_input_rect.x + 5, confirmedPassword_input_rect.y + 2))
        # ^^^ draw cpass text surface at rectangle coordinates
        confirmedPassword_input_rect.w = max(300, displayedcpasstext_surface.get_width() + 10)
        # ^^^ Allow width of rectangle entry box to stretch
        if confirmedPassword_input_rect.w == 540:  # Make a maximum width for rectangle
            confirmedPassword_input_rect.w = 540

        # Message Handling (Success or Error)
        if show_registerError_message:  # Checking that error message is true (if requirements from function weren't met)
            draw_text("Please fill username, password must contain 1 symbol,", font4, TEXT_COL3, 185, 525)
            draw_text("1 letter, 1 number and must be 5 or more characters long", font4, TEXT_COL3, 160, 547)
            draw_text("Username may already be taken", font4, TEXT_COL3, 432, 570)
            # Draw the text that states requirements
            if time.time() - registerErrorMessage_timestamp >= 10:  # Check that the time recorded subtracted by timestamp is
                # ^^^ greater than or equal to 10
                show_registerError_message = False
                # ^^^ If so, error message set to false so the text disappears
        if show_registerSuccess_message:  # Same logic as the previous time based error message
            draw_text("Account Successfully Saved, Go To Login!", font4, TEXT_COL4, 325, 562)
            if time.time() - registerSuccessMessage_timestamp >= 10:
                show_registerSuccess_message = False
        if show_registerSuccess_message and show_registerError_message and \
                time.time() - registerErrorMessage_timestamp > time.time() - registerSuccessMessage_timestamp:
            show_registerError_message = False
            show_registerSuccess_message = True
        #  These 2 functions between this comment are being used to check for the error and success messages co-existing
        #  These if statements are meant to prevent that from happening so the latest message is visible while the other
        #  isn't.
        if show_registerSuccess_message and show_registerError_message and \
                time.time() - registerSuccessMessage_timestamp > time.time() - registerErrorMessage_timestamp:
            show_registerSuccess_message = False
            show_registerError_message = True

        #  Active and Passive border colouring
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

        # Creating button instances using the second button class
        REGISTER_BACK = Button2(image=pygame.image.load("backButton.png"), pos=(0, 0),
                                text_input="", font=get_font(1), base_color="Black", hovering_color="Black", scale=0.1)
        DELETE_USERNAME = Button2(image=pygame.image.load("deleteButton.png"), pos=(username_input_rect.right,
                                                                                    username_input_rect.topright[1]),
                                  text_input="DELETE", font=get_font(15), base_color="White", hovering_color="Grey", scale=0.325)
        DELETE_PASSWORD = Button2(image=pygame.image.load("deleteButton.png"), pos=(password_input_rect.right,
                                                                                    password_input_rect.topright[1]),
                                  text_input="DELETE", font=get_font(15), base_color="White", hovering_color="Grey", scale=0.325)
        DELETE_CPASSWORD = Button2(image=pygame.image.load("deleteButton.png"), pos=(confirmedPassword_input_rect.right,
                                                                                     confirmedPassword_input_rect.topright[1]),
                                   text_input="DELETE", font=get_font(15), base_color="White", hovering_color="Grey", scale=0.325)
        SUBMIT_BUTTON = Button2(image=pygame.image.load("submitButton.png"), pos=(654, 0),
                                text_input="SUBMIT", font=get_font(25), base_color="White", hovering_color="Grey", scale=0.4)
        for buttons in [REGISTER_BACK, DELETE_USERNAME, DELETE_PASSWORD, DELETE_CPASSWORD, SUBMIT_BUTTON]:
            buttons.changeColor(InitialMenu_mouse_pos)
            buttons.update(screen)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if REGISTER_BACK.checkForInput(InitialMenu_mouse_pos):
                    initial_menu()
                if DELETE_USERNAME.checkForInput(InitialMenu_mouse_pos):
                    user_text = ""
                if DELETE_PASSWORD.checkForInput(InitialMenu_mouse_pos):
                    pass_text = ""
                    displayed_pass_text = ""
                if DELETE_CPASSWORD.checkForInput(InitialMenu_mouse_pos):
                    confirmedPassword_text = ""
                    displayed_confirmedPassword_text = ""
                if SUBMIT_BUTTON.checkForInput(InitialMenu_mouse_pos):
                    if len(pass_text) >= 5 and confirmedPassword_text == pass_text and \
                            contains_alpha_digits_and_symbols(pass_text) is True and \
                            contains_alpha_digits_and_symbols(confirmedPassword_text) is True and \
                            user_text != "Enter Username" and len(user_text) >= 1 and not user_validating(user_text):
                        addAccount(user_text, pass_text)
                        show_registerSuccess_message = True
                        registerSuccessMessage_timestamp = time.time()
                        # RESET ALL TEXT VARIABLES
                        user_text = "Enter Username"
                        displayed_pass_text = "Enter Password"
                        displayed_confirmedPassword_text = "Enter Password Again"
                        pass_text = ""
                        confirmedPassword_text = ""
                        username_active = False  # Mention this in word documentation
                        password_active = False
                        confirmedPassword_active = False
                    else:
                        show_registerError_message = True  # Make error message variable true
                        registerErrorMessage_timestamp = time.time()  # As variable becomes true, time will be recorded
                        # RESET ALL TEXT VARIABLES
                        user_text = "Enter Username"
                        displayed_pass_text = "Enter Password"
                        displayed_confirmedPassword_text = "Enter Password Again"
                        pass_text = ""
                        confirmedPassword_text = ""

                if event.type == pygame.MOUSEBUTTONDOWN:  # Checks for event that indicates user clicks with mouse
                    if username_input_rect.collidepoint(event.pos):  # checks its colliding with the user input rect
                        username_active = True  # if so username active is set to True
                        if user_text == "Enter Username":  # If text variable is the default text
                            user_text = ""  # Set the text variable to nothing when the entry box is clicked.
                    else:
                        username_active = False  # Otherwise it remains False
                    if password_input_rect.collidepoint(event.pos):
                        password_active = True
                        if displayed_pass_text == "Enter Password":
                            displayed_pass_text = ""
                    else:
                        password_active = False
                    if confirmedPassword_input_rect.collidepoint(event.pos):
                        confirmedPassword_active = True
                        if displayed_confirmedPassword_text == "Enter Password Again":
                            displayed_confirmedPassword_text = ""
                    else:
                        confirmedPassword_active = False

            mods = pygame.key.get_mods()
            if event.type == pygame.KEYDOWN and username_active is True:
                # ^^^ Check event is a key being pressed and username entrybox is active
                if len(user_text) < 20:  # Check length of text is NOT equal to max characters
                    if event.key == pygame.K_TAB:  # If key is Tab
                        pass  # Ignore and don't do anything
                    elif event.key == pygame.K_DELETE:  # Otherwise If key is delete
                        pass  # Ignore and don't do anything
                    elif event.key == pygame.K_RETURN:  # Otherwise If key is enter
                        username_active = False  # Make active false
                    elif event.key == pygame.K_BACKSPACE:  # Otherwise if key is a backspace
                        user_text = user_text[:-1]  # Subtract 1 from end of text using indexing
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.unicode and mods & pygame.KMOD_LCTRL or mods & pygame.KMOD_RCTRL:  # If control is being held while clicking any key
                        pass
                    else:
                        user_text += event.unicode  # Otherwise add unicode since not max characters
                else:  # Otherwise (text is equal to max characters)
                    if event.key == pygame.K_RETURN:  # Check key is return
                        username_active = False  # Make active false
                    if event.key == pygame.K_BACKSPACE:  # Check key is backspace
                        user_text = user_text[:-1]  # Subtract 1 from end of text using indexing
                    if event.key == pygame.K_TAB:  # If key is Tab
                        pass  # Ignore and don't do anything
                    if event.key == pygame.K_DELETE:  # If key is delete
                        pass  # Ignore and don't do anything

            if event.type == pygame.KEYDOWN and password_active is True:  # Same logic
                if len(pass_text) < 20:
                    if event.key == pygame.K_TAB:
                        pass
                    elif event.key == pygame.K_DELETE:
                        pass
                    elif event.key == pygame.K_RETURN:
                        password_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        pass_text = pass_text[:-1]
                        displayed_pass_text = displayed_pass_text[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.unicode and mods & pygame.KMOD_LCTRL or mods & pygame.KMOD_RCTRL:
                        pass
                    elif event.unicode:  # Instead we check that this statement is true meaning the user is entering text
                        displayed_pass_text += "*"  # Add the censored version for the other text variable
                        pass_text += event.unicode  # Continue to add whatever they are actually entering
                        # ^^^ While the previous elif statements allow us to backspace, ignore 'DELETE' etc.
                else:
                    if event.key == pygame.K_RETURN:
                        password_active = False
                    if event.key == pygame.K_BACKSPACE:
                        pass_text = pass_text[:-1]
                        displayed_pass_text = displayed_pass_text[:-1]
                    if event.key == pygame.K_TAB:
                        pass
                    if event.key == pygame.K_DELETE:
                        pass

            if event.type == pygame.KEYDOWN and confirmedPassword_active is True:  # Same logic
                if len(confirmedPassword_text) < 20:
                    if event.key == pygame.K_TAB:
                        pass
                    elif event.key == pygame.K_DELETE:
                        pass
                    elif event.key == pygame.K_RETURN:
                        confirmedPassword_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        confirmedPassword_text = confirmedPassword_text[:-1]
                        displayed_confirmedPassword_text = displayed_confirmedPassword_text[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.unicode and mods & pygame.KMOD_LCTRL or mods & pygame.KMOD_RCTRL:
                        pass
                    elif event.unicode:
                        displayed_confirmedPassword_text += "*"
                        confirmedPassword_text += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        confirmedPassword_active = False
                    if event.key == pygame.K_BACKSPACE:
                        confirmedPassword_text = confirmedPassword_text[:-1]
                        displayed_confirmedPassword_text = displayed_confirmedPassword_text[:-1]
                    if event.key == pygame.K_TAB:
                        pass
                    if event.key == pygame.K_DELETE:
                        pass

        pygame.display.update()
        clock.tick(FPS)

def login():
    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # defining screen / display surface with height and width
    while True:
        screen.fill((90, 157, 157))
        InitialMenu_mouse_pos = pygame.mouse.get_pos()

        draw_text("Login", font5, TEXT_COL, 85, 45)
        draw_text("Username", font3, TEXT_COL, 85, 225)
        draw_text("Password", font3, TEXT_COL, 85, 390)

        global loginPass_text
        global loginUser_text
        global loginUsername_active
        global loginDisplayed_pass_text
        global loginPassword_active
        global loginUserBorderColor
        global loginPassBorderColor
        global show_loginError_message
        global loginPass_text

        #  username text surface
        if loginUser_text == "" and loginUsername_active is False:  # Must check that the text is not being entered
            loginUser_text = "Enter Username"  # If its empty nothing + it being entered then it'll set to 'Enter Username'
        if loginUser_text == "Enter Username":
            loginUsertext_surface = user_font.render(loginUser_text, True, TEXT_COL2)
            # ^^^ Define text surface to be drawn to screen for username
        else:
            loginUsertext_surface = user_font.render(loginUser_text, True, TEXT_COL)

        #  password text surface
        if loginDisplayed_pass_text == "" and loginPassword_active is False:  # Similar scenario as above
            loginDisplayed_pass_text = "Enter Password"
        if loginDisplayed_pass_text == "Enter Password":
            loginDisplayedpasstext_surface = user_font.render(loginDisplayed_pass_text, True, TEXT_COL2)
        else:
            loginDisplayedpasstext_surface = user_font.render(loginDisplayed_pass_text, True, TEXT_COL)

        #  Entry Box for Username
        pygame.draw.rect(screen, loginUserBorderColor, loginUsername_input_rect)
        # ^^^ Draw the username input rectangle to the screen
        screen.blit(loginUsertext_surface, (loginUsername_input_rect.x + 5, loginUsername_input_rect.y + 2))
        # ^^^ Draw to screen the username text surface at rectangle coordinates
        loginUsername_input_rect.w = max(300, loginUsertext_surface.get_width() + 10)
        # ^^^ Allow width of rectangle entry box to stretch
        if loginUsername_input_rect.w == 540:  # Make a maximum width for rectangle
            loginUsername_input_rect.w = 540

        #  Entry Box for Password
        pygame.draw.rect(screen, loginPassBorderColor, loginPassword_input_rect)
        # ^^^ Draw the password input rectangle to the screen
        screen.blit(loginDisplayedpasstext_surface, (loginPassword_input_rect.x + 5, loginPassword_input_rect.y + 2))
        # ^^^ draw to screen the password text surface at rectangle coordinates
        loginPassword_input_rect.w = max(300, loginDisplayedpasstext_surface.get_width() + 10)
        # ^^^ Allow width of rectangle entry box to stretch
        if loginPassword_input_rect.w == 540:  # Make a maximum width for rectangle
            loginPassword_input_rect.w = 540

        # Button instances
        LOGIN_BACK = Button2(image=pygame.image.load("backButton.png"), pos=(0, 0),
                             text_input="", font=font7, base_color="Black", hovering_color="Black", scale=0.1)
        LOGIN_DELETE_USERNAME = Button2(image=pygame.image.load("deleteButton.png"), pos=(loginUsername_input_rect.right,
                                                                                    loginUsername_input_rect.topright[1]),
                                  text_input="DELETE", font=get_font(15), base_color="White", hovering_color="Grey", scale=0.32)
        LOGIN_DELETE_PASSWORD = Button2(image=pygame.image.load("deleteButton.png"), pos=(loginPassword_input_rect.right,
                                                                                    loginPassword_input_rect.topright[1]),
                                  text_input="DELETE", font=get_font(15), base_color="White", hovering_color="Grey", scale=0.32)
        LOGIN_SUBMIT_BUTTON = Button2(image=pygame.image.load("submitButton.png"), pos=(654, 0), text_input="SUBMIT",
                                font=get_font(25), base_color="White", hovering_color="Grey", scale=0.4)

        for button in [LOGIN_BACK, LOGIN_DELETE_USERNAME, LOGIN_DELETE_PASSWORD, LOGIN_SUBMIT_BUTTON]:
            button.changeColor(InitialMenu_mouse_pos)
            button.update(screen)

        #  Message handling
        if show_loginError_message:
            draw_text("Invalid Information, Please Try Again", font4, TEXT_COL3, 375, 560)
            global loginErrorMessage_timestamp
            if time.time() - loginErrorMessage_timestamp >= 10:
                show_loginError_message = False

        #  Active and Passive Border Colouring
        if loginUsername_active:  # Checks username active is True
            loginUserBorderColor = borderColor_active  # Sets it to active border colour
        if loginUsername_active is False:  # Checks if username active is False
            loginUserBorderColor = borderColor_passive  # Sets it to passive border colour
        if loginPassword_active:
            loginPassBorderColor = borderColor_active
        if loginPassword_active is False:
            loginPassBorderColor = borderColor_passive

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if LOGIN_BACK.checkForInput(InitialMenu_mouse_pos):
                    initial_menu()
                if LOGIN_DELETE_USERNAME.checkForInput(InitialMenu_mouse_pos):
                    loginUser_text = ""
                if LOGIN_DELETE_PASSWORD.checkForInput(InitialMenu_mouse_pos):
                    loginPass_text = ""
                    loginDisplayed_pass_text = ""
                if LOGIN_SUBMIT_BUTTON.checkForInput(InitialMenu_mouse_pos):
                    if login_validating(loginUser_text, loginPass_text):
                        global accountDetails
                        accountDetails = (loginUser_text, loginPass_text)  # In main menu, you will always reference the players
                        #  account to be with these details, this username and password, since the login validating function
                        #  outputs true
                        #  RESET TEXT VARIABLES
                        loginUser_text = ""
                        loginPass_text = ""
                        loginDisplayed_pass_text = ""
                        loginUsername_active = False
                        loginPassword_active = False
                        main_menu()
                    else:
                        show_loginError_message = True
                        loginErrorMessage_timestamp = time.time()
                        #  RESET TEXT VARIABLES
                        loginUser_text = ""
                        loginPass_text = ""
                        loginDisplayed_pass_text = ""

                if loginUsername_input_rect.collidepoint(event.pos):
                    loginUsername_active = True
                    if loginUser_text == "Enter Username":
                        loginUser_text = ""
                else:
                    loginUsername_active = False
                if loginPassword_input_rect.collidepoint(event.pos):
                    loginPassword_active = True
                    if loginDisplayed_pass_text == "Enter Password":
                        loginDisplayed_pass_text = ""
                else:
                    loginPassword_active = False

            mods = pygame.key.get_mods()
            if event.type == pygame.KEYDOWN and loginUsername_active is True:  # Same logic
                if len(loginUser_text) < 20:
                    if event.key == pygame.K_TAB:
                        pass
                    elif event.key == pygame.K_DELETE:
                        pass
                    elif event.key == pygame.K_RETURN:
                        loginUsername_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        loginUser_text = loginUser_text[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.unicode and mods & pygame.KMOD_LCTRL or mods & pygame.KMOD_RCTRL:
                        pass
                    else:
                        loginUser_text += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        loginUsername_active = False
                    if event.key == pygame.K_BACKSPACE:
                        loginUser_text = loginUser_text[:-1]
                    if event.key == pygame.K_TAB:
                        pass
                    if event.key == pygame.K_DELETE:
                        pass

            if event.type == pygame.KEYDOWN and loginPassword_active is True:  # Same logic
                if len(loginPass_text) < 20:
                    if event.key == pygame.K_TAB:
                        pass
                    elif event.key == pygame.K_DELETE:
                        pass
                    elif event.key == pygame.K_RETURN:
                        loginPassword_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        loginPass_text = loginPass_text[:-1]
                        loginDisplayed_pass_text = loginDisplayed_pass_text[:-1]
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.unicode and mods & pygame.KMOD_LCTRL or mods & pygame.KMOD_RCTRL:
                        pass
                    elif event.unicode:
                        loginDisplayed_pass_text += "*"
                        loginPass_text += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        loginPassword_active = False
                    if event.key == pygame.K_BACKSPACE:
                        loginPass_text = loginPass_text[:-1]
                        loginDisplayed_pass_text = loginDisplayed_pass_text[:-1]
                    if event.key == pygame.K_TAB:
                        pass
                    if event.key == pygame.K_DELETE:
                        pass

        pygame.display.update()
        clock.tick(FPS)

def main_menu():
    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # defining screen / display surface with height and width
    while True:

        screen.fill((90, 157, 157))
        MainMenu_mouse_pos = pygame.mouse.get_pos()

        global mainMenu_music_playing

        if mainMenu_music_playing is False:  # Variable should be false initially or if we clicked back to login
            main_menu_music.set_volume(1)  # Set volume to max
            main_menu_music.play(-1)  # Infinitely loops music (-1)
            mainMenu_music_playing = True  # Set music playing to true so that it wont repeat itself unless we click back to login

        wave_rect = MainMenu.MainMenuGui(-10, 280, MainMenu.wave_img, 1)  # Using class from main menu code file for gui
        wave_rect.draw(screen)
        draw_text("Eldritch", font6, TEXT_COL5, 5, 10)  # Draw text function
        draw_text("Echoes", font6, TEXT_COL5, 5, 175)  # Draw text function

        # Button instances
        PLAY_BUTTON = Button2(image=pygame.image.load("MainMenuButtonRects.png"), pos=(480, 20), text_input="PLAY",
                              font=get_font(20), base_color=(90, 157, 157), hovering_color="White", scale=1)
        CUSTOMIZATION_BUTTON = Button2(image=pygame.image.load("MainMenuButtonRects.png"), pos=(480, PLAY_BUTTON.rect.bottomleft[1]),
                                       text_input="CUSTOMIZE", font=get_font(20), base_color=(90, 157, 157),
                                       hovering_color="White",
                                       scale=1)
        LEADERBOARD_BUTTON = Button2(image=pygame.image.load("MainMenuButtonRects.png"), pos=(480, CUSTOMIZATION_BUTTON.rect.bottomleft[1]),
                                     text_input="LEADERBOARD", font=get_font(20), base_color=(90, 157, 157),
                                     hovering_color="White",
                                     scale=1)
        SETTINGS_BUTTON = Button2(image=pygame.image.load("MainMenuButtonRects.png"), pos=(480, LEADERBOARD_BUTTON.rect.bottomleft[1]),
                                  text_input="SETTINGS", font=get_font(20), base_color=(90, 157, 157),
                                  hovering_color="White",
                                  scale=1)
        TUTORIAL_BUTTON = Button2(image=pygame.image.load("MainMenuButtonRects.png"), pos=(480, SETTINGS_BUTTON.rect.bottomleft[1]),
                                  text_input="TUTORIAL", font=get_font(20), base_color=(90, 157, 157),
                                  hovering_color="White",
                                  scale=1)
        MAIN_MENU_BACK = Button2(image=pygame.image.load("MainMenuButtonRects.png"), pos=(480, TUTORIAL_BUTTON.rect.bottomleft[1]),
                                 text_input="BACK TO LOGIN", font=get_font(20), base_color=(90, 157, 157),
                                 hovering_color="White", scale=1)
        for buttons in [MAIN_MENU_BACK, PLAY_BUTTON, CUSTOMIZATION_BUTTON, TUTORIAL_BUTTON, SETTINGS_BUTTON, LEADERBOARD_BUTTON]:
            buttons.changeColor(MainMenu_mouse_pos)
            buttons.update(screen)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PLAY_BUTTON.checkForInput(MainMenu_mouse_pos):
                    main_menu_music.stop()
                    mainMenu_music_playing = False
                    if __name__ == '__main__':
                        game = Game()  # Sets game variable to game class
                        game.run()  # Executes run method of game class
                if CUSTOMIZATION_BUTTON.checkForInput(MainMenu_mouse_pos):
                    # customize()
                    print("Customize")
                if LEADERBOARD_BUTTON.checkForInput(MainMenu_mouse_pos):
                    # leaderboard()
                    main_menu_music.stop()
                    mainMenu_music_playing = False
                    if __name__ == '__main__':
                        leaderboard = Leaderboard(font8)
                        leaderboard.run()
                if SETTINGS_BUTTON.checkForInput(MainMenu_mouse_pos):
                    # settings()
                    print("Settings")
                if TUTORIAL_BUTTON.checkForInput(MainMenu_mouse_pos):
                    # tutorial()
                    main_menu_music.stop()
                    mainMenu_music_playing = False
                    if __name__ == '__main__':
                        tutorial = Tutorial(font8)
                        tutorial.run()
                if MAIN_MENU_BACK.checkForInput(MainMenu_mouse_pos):
                    main_menu_music.stop()
                    mainMenu_music_playing = False
                    login()

        pygame.display.update()
        clock.tick(FPS)

class Leaderboard:
    def __init__(self, font):
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.data = get_leaderboard_info()
        self.items = {index: f"{username} :  {damage}" for index, (username, damage) in enumerate(self.data)}

        # dimensions
        self.main_rect = pygame.FRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # list
        self.rows = 3
        self.list_width = self.main_rect.width
        self.item_height = self.main_rect.height / self.rows
        self.index = 0
        self.selected_index = None

    def input(self):
        if len(self.items) > 0:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_UP]:
                self.index -= 1
            if keys[pygame.K_DOWN]:
                self.index += 1
            self.index = self.index % len(self.items)

    def display_list(self):
        bg_rect = pygame.FRect(self.main_rect.topleft, (self.list_width, self.main_rect.height))
        pygame.draw.rect(self.display_surface, (90, 157, 157), bg_rect)

        if len(self.items) > 0:
            v_offset = 0 if self.index < self.rows else -(self.index - self.rows + 1) * self.item_height
            for index, item in self.items.items():
                # colors
                if self.index != index:
                    bg_color = (90, 157, 157)
                else:
                    bg_color = 'light gray'

                text_color = 'Black'

                top = self.main_rect.top + index * self.item_height + v_offset  # depending on index, the top will be lower and lower
                item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

                text_surf = self.font.render(item, False, text_color)
                text_rect = text_surf.get_frect(midleft=item_rect.midleft + vector(45, 0))

                if item_rect.colliderect(self.main_rect):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)

                    self.display_surface.blit(text_surf, text_rect)

            # lines
            for i in range(min(self.rows, len(self.items))):
                y = self.main_rect.top + self.item_height * i
                left = self.main_rect.left
                right = self.main_rect.left + self.list_width
                pygame.draw.line(self.display_surface, 'black', (left, y), (right, y))

            # shadow
            shadow_surf = pygame.Surface((4, self.main_rect.height))
            shadow_surf.set_alpha(100)
            self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top))

    def run(self):
        while True:
            self.input()
            self.display_list()
            self.mouse_pos = pygame.mouse.get_pos()

            MAIN_MENU_BACK = Button2(image=pygame.image.load("backButton.png"), pos=(0, 0),
                                     text_input="", font=font7, base_color="Black", hovering_color="Black", scale=0.1)
            MAIN_MENU_BACK.changeColor(self.mouse_pos)
            MAIN_MENU_BACK.update(self.display_surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if MAIN_MENU_BACK.checkForInput(self.mouse_pos):
                        main_menu()

            pygame.display.update()

class Tutorial:
    def __init__(self, font):
        self.display_surface = pygame.display.get_surface()
        self.font = font

        # dimensions
        self.main_rect = pygame.FRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def display_list(self):
        bg_rect = pygame.FRect(self.main_rect.topleft, (self.main_rect.width, self.main_rect.height))
        pygame.draw.rect(self.display_surface, (90, 157, 157), bg_rect)

        bg_color = (90, 157, 157)

        text_color = 'Black'

        item = "How to play:"
        item2 = "Talk to the mermaid NPC for your quest."
        item3 = "When a quest is complete, walk over to the pirate ship to "
        item4 = "go to the next island"
        item5 = "Enemy NPC's are always near an X mark"
        item6 = "Controls:"
        item7 = "Movement - WASD / Arrow Keys"
        item8 = "Select / Interact - Space"
        item9 = "Scroll - Up / Down Arrow Keys"
        item10 = "Menu / Options - Escape"
        item_rect = pygame.FRect(self.main_rect.left, self.main_rect.top, self.main_rect.width, self.main_rect.height)

        text_surf1 = self.font.render(item, False, text_color)
        text_rect1 = text_surf1.get_frect(topleft=item_rect.topleft + vector(10, 90))
        text_surf2 = self.font.render(item2, False, text_color)
        text_rect2 = text_surf2.get_frect(topleft=item_rect.topleft + vector(10, 150))
        text_surf3 = self.font.render(item3, False, text_color)
        text_rect3 = text_surf3.get_frect(topleft=item_rect.topleft + vector(10, 190))
        text_surf4 = self.font.render(item4, False, text_color)
        text_rect4 = text_surf4.get_frect(topleft=item_rect.topleft + vector(10, 230))
        text_surf5 = self.font.render(item5, False, text_color)
        text_rect5 = text_surf5.get_frect(topleft=item_rect.topleft + vector(10, 270))
        text_surf6 = self.font.render(item6, False, text_color)
        text_rect6 = text_surf6.get_frect(topleft=item_rect.topleft + vector(10, 330))
        text_surf7 = self.font.render(item7, False, text_color)
        text_rect7 = text_surf7.get_frect(topleft=item_rect.topleft + vector(10, 390))
        text_surf8 = self.font.render(item8, False, text_color)
        text_rect8 = text_surf8.get_frect(topleft=item_rect.topleft + vector(10, 430))
        text_surf9 = self.font.render(item9, False, text_color)
        text_rect9 = text_surf9.get_frect(topleft=item_rect.topleft + vector(10, 470))
        text_surf10 = self.font.render(item10, False, text_color)
        text_rect10 = text_surf10.get_frect(topleft=item_rect.topleft + vector(10, 510))

        if item_rect.colliderect(self.main_rect):
            pygame.draw.rect(self.display_surface, bg_color, item_rect)

            self.display_surface.blit(text_surf1, text_rect1)
            self.display_surface.blit(text_surf2, text_rect2)
            self.display_surface.blit(text_surf3, text_rect3)
            self.display_surface.blit(text_surf4, text_rect4)
            self.display_surface.blit(text_surf5, text_rect5)
            self.display_surface.blit(text_surf6, text_rect6)
            self.display_surface.blit(text_surf7, text_rect7)
            self.display_surface.blit(text_surf8, text_rect8)
            self.display_surface.blit(text_surf9, text_rect9)
            self.display_surface.blit(text_surf10, text_rect10)

    def run(self):
        while True:
            self.display_list()
            self.mouse_pos = pygame.mouse.get_pos()

            MAIN_MENU_BACK = Button2(image=pygame.image.load("backButton.png"), pos=(0, 0),
                                     text_input="", font=font7, base_color="Black", hovering_color="Black", scale=0.1)
            MAIN_MENU_BACK.changeColor(self.mouse_pos)
            MAIN_MENU_BACK.update(self.display_surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if MAIN_MENU_BACK.checkForInput(self.mouse_pos):
                        main_menu()

            pygame.display.update()

class Game:
    # general
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        pygame.display.set_caption("Eldritch Echoes")
        self.clock = pygame.time.Clock()
        self.accountDetails = accountDetails

        self.load_account_data()

        self.player_image = pygame.image.load('Player_img.png')

        self.battle_music = pygame.mixer.Sound('BattleMusic.ogg')
        self.battle_music_playing = False

        self.spirit_battle_music = pygame.mixer.Sound('BattleMusicSpirit.ogg')
        self.spirit_battle_music_playing = False

        self.marduk_battle_music = pygame.mixer.Sound('BattleMusicMarduk.ogg')
        self.marduk_battle_music_playing = False

        self.gold = 0
        self.inventory_dict = {0: 'Dagger'}
        self.equipped_weapon = 'Dagger'
        self.equipped_armour = None
        self.battle = None
        self.damage = 0

        # player monsters
        self.opposing_monsters = {
            0: Monster('animal', 30),
            1: Monster('shark', 29),
            2: Monster('captain_dreadful', 50),
            3: Monster('spirit', 100),
            4: Monster('captain_marduk', 110),
        }

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        # transition / tint
        self.transition_target = 'abc'
        self.tint_surf = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600

        # import map assets
        self.import_assets()  # running import assests method
        self.player_pos = check_player_pos(accountDetails[0])
        self.setup(self.tmx_maps['EldritchEchoesMap('+self.player_pos+')'], self.player_pos)  # collecting from dictionary in import assets method

        self.dialog_tree = None  # initially set to neither true or false

        # overlays
        self.dialog_tree = None
        self.monster_index = MonsterIndex(self.opposing_monsters, self.fonts, self.monster_frames)
        self.index_open = False
        self.mini_menu = MiniMenu(self.fonts, main_menu, self)
        self.menu_open = False
        self.inventory = Inventory(self.fonts, self)
        self.inventory_open = False
        self.stats_menu = Stats_menu(self.fonts, self)
        self.stats_menu_open = False

        # battles
        self.battle_animal = Battle(self.opposing_monsters[0], self.monster_frames['battle_icons']['animal'],
                             self.fonts['regular'], self, self.monster_frames, self.audio)
        self.battle_shark = Battle(self.opposing_monsters[1], self.monster_frames['battle_icons']['shark'],
                             self.fonts['regular'], self, self.monster_frames, self.audio)
        self.battle_captain_dreadful = Battle(self.opposing_monsters[2], self.monster_frames['battle_icons']['captain_dreadful'],
                             self.fonts['regular'], self, self.monster_frames, self.audio)
        self.battle_spirit = Battle(self.opposing_monsters[3], self.monster_frames['battle_icons']['spirit'],
                             self.fonts['regular'], self, self.monster_frames, self.audio)
        self.battle_captain_marduk = Battle(self.opposing_monsters[4], self.monster_frames['battle_icons']['captain_marduk'],
                             self.fonts['regular'], self, self.monster_frames, self.audio)

    def import_assets(self):
        self.fonts = {
            'dialog': pygame.font.Font(join('PixeloidSans.ttf'), 15),
            'regular': pygame.font.Font(join('PixeloidSans.ttf'), 15),
            'regular2': pygame.font.Font(join('PixeloidSans.ttf'), 25),
            'small': pygame.font.Font(join('PixeloidSans.ttf'), 2),
            'bold': pygame.font.Font(join('dogicapixelbold.otf'), 15),
            'bold2': pygame.font.Font(join('dogicapixelbold.otf'), 50)
        }

        self.monster_frames = {
            'icons': import_folder_dict('icons'),
            'battle_icons': import_folder_dict('battle_icons'),
            'attacks': attack_importer('Attacks')
        }

        self.tmx_maps = {
            'EldritchEchoesMap(island1)': load_pygame('EldritchEchoesMap.tmx'),
            'EldritchEchoesMap(island2)': load_pygame('EldritchEchoesMap(island2).tmx'),
            'EldritchEchoesMap(island3)': load_pygame('EldritchEchoesMap(island3).tmx'),
            'EldritchEchoesMap(island4)': load_pygame('EldritchEchoesMap(island4).tmx') # create dictionary for different maps
        }

        self.battle_bg = import_folder_dict('graphic')

        self.audio = audio_importer('audio')

    def setup(self, tmx_map, player_start_pos):
        self.player_start_pos = player_start_pos

        # clear the map
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
            group.empty()

        # floor
        for layer in ['Floor', 'Details']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():  # search through tile layer 'floor'
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])  # create sprite of all tiles in floor layer

        # objects
        for obj in tmx_map.get_layer_by_name('Objects') + tmx_map.get_layer_by_name('Objects2'):  # search through object layer 'Objects', this will be a list concatenated with objects 2
            if obj.name == 'top':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])  # create regular sprite for any objects with the name 'top'
            elif obj.name == 'Flag1':
                surf = pygame.image.load('Tiles/087.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'Flag2':
                surf = pygame.image.load('Tiles/087.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'Flag3':
                surf = pygame.image.load('Tiles/087.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'Flag4':
                surf = pygame.image.load('Tiles/087.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'barrel1':
                surf = pygame.image.load('Tiles/102.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'barrel2':
                surf = pygame.image.load('Tiles/102.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'barrel3':
                surf = pygame.image.load('Tiles/102.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'barrel4':
                surf = pygame.image.load('Tiles/102.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'barrel5':
                surf = pygame.image.load('Tiles/102.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'barrel6':
                surf = pygame.image.load('Tiles/102.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest1':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest2':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest3':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest4':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest5':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest6':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            elif obj.name == 'chest7':
                surf = pygame.image.load('Tiles/135.png')
                Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites),
                          ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
            else:
                CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))  # create collidable sprite (slightly different hitbox)

        for x, y, surf in tmx_map.get_layer_by_name('FloorBlocks').tiles():  # floorblocks are the barrier not allowing player to leave an island into the ocean
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.collision_sprites)

        # transition objects
        for obj in tmx_map.get_layer_by_name('Transition'):
            TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos'], obj.properties['mermaid']), self.transition_sprites)

        # entities
        for obj in tmx_map.get_layer_by_name('Entities'):  # search through object layer 'entities'
            # Player
            if obj.name == 'Player':  # check if object is player object
                if obj.properties['pos'] == player_start_pos:  # check object meets player criteria
                    surf = pygame.image.load('Player_img.png')
                    self.player = Player((obj.x, obj.y), surf, self.all_sprites, self.collision_sprites)
                    # ^^^ Create player from objects (its only if objects name=player)
            # Characters
            else:
                # Render each character using the character class
                if obj.name == 'Mermaid':
                    surf = pygame.image.load('Tiles/124.png')
                    Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites), ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
                if obj.name == 'Shark':
                    surf = pygame.image.load('Tiles/120.png')
                    Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites), ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
                if obj.name == 'Animal':
                    surf = pygame.image.load('Tiles/103.png')
                    Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites), ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
                if obj.name == 'Captain_dreadful':
                    surf = pygame.image.load('Tiles/127.png')
                    Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites), ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
                if obj.name == 'Captain_marduk':
                    surf = pygame.image.load('Tiles/126.png')
                    Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites), ENEMY_DATA[obj.properties['character_id']], accountDetails, self)
                if obj.name == 'Spirit':
                    surf = pygame.image.load('Tiles/122.png')
                    Character((obj.x, obj.y), surf, (self.all_sprites, self.collision_sprites, self.character_sprites), ENEMY_DATA[obj.properties['character_id']], accountDetails, self)

    # dialog system
    def input(self):
        if not self.dialog_tree and not self.battle:  # dialog tree is not true neither is self.battle
            keys = pygame.key.get_just_pressed()  # collect the players entered keys that are only just newly pressed
            if keys[pygame.K_SPACE] and self.menu_open is False and self.index_open is False and self.inventory_open is False and self.stats_menu_open is False:  # if the key pressed is space
                for character in self.character_sprites:  # for all characters in character sprites
                    if check_connections(50, self.player, character):  # if the check connections function in radius 50 for the player and the character is handed in
                        #^^^ check connections being true means that the character is in the radius of the player
                        # block player input
                        self.player.block()  # block the players input completely
                        # create dialog
                        self.create_dialog(character)  # use create dialog function on the character thats in the radius of the player as the player clicks space

            elif keys[pygame.K_RETURN] and self.menu_open is False and self.inventory_open is False and \
                    self.stats_menu_open is False and self.tint_mode != 'tint':
                self.index_open = not self.index_open
                self.player.blocked = not self.player.blocked

            elif keys[pygame.K_ESCAPE] and self.index_open is False and self.tint_mode != 'tint':
                self.menu_open = not self.menu_open
                self.player.blocked = not self.player.blocked

    def create_dialog(self, character):
        if not self.dialog_tree:  # dialog tree is not true
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)  # set dialog tree to the class with the arguments specified

    def end_dialog(self, character):
        self.dialog_tree = None  # When ending the dialog, dialog tree should be set to nothing again
        self.player.unblock()  # unblock the player so input can be collected again

        if not character.character_data['defeated']:
            # check for combat initiation for combat overlays
            if ENEMY_DATA['o1']['in_combat']:
                self.transition_target = Battle(self.opposing_monsters[0], self.monster_frames['battle_icons']['animal'],
                                self.fonts['regular'], self, self.monster_frames, self.audio)
                self.tint_mode = 'tint'
            elif ENEMY_DATA['o2']['in_combat']:
                self.transition_target = Battle(self.opposing_monsters[1], self.monster_frames['battle_icons']['shark'],
                               self.fonts['regular'], self, self.monster_frames, self.audio)
                self.tint_mode = 'tint'
            elif ENEMY_DATA['o3']['in_combat']:
                self.transition_target = Battle(self.opposing_monsters[2],
                                          self.monster_frames['battle_icons']['captain_dreadful'],
                                          self.fonts['regular'], self, self.monster_frames, self.audio)
                self.tint_mode = 'tint'
            elif ENEMY_DATA['o4']['in_combat']:
                self.transition_target = Battle(self.opposing_monsters[3], self.monster_frames['battle_icons']['spirit'],
                                self.fonts['regular'], self, self.monster_frames, self.audio)
                self.tint_mode = 'tint'
            elif ENEMY_DATA['o5']['in_combat']:
                self.transition_target = Battle(self.opposing_monsters[4],
                                        self.monster_frames['battle_icons']['captain_marduk'],
                                        self.fonts['regular'], self, self.monster_frames, self.audio)
                self.tint_mode = 'tint'

    # transition system
    def transition_check(self):
        if self.player_start_pos[:7] == 'island1':
            if ENEMY_DATA['o1']['defeated'] and ENEMY_DATA['o2']['defeated']:
                ENEMY_DATA['m1']['complete'] = True
        if self.player_start_pos[:7] == 'island2':
            if ENEMY_DATA['o3']['defeated']:
                ENEMY_DATA['m2']['complete'] = True
        if self.player_start_pos[:7] == 'island3':
            if ENEMY_DATA['o4']['defeated']:
                ENEMY_DATA['m3']['complete'] = True
        if self.player_start_pos[:7] == 'island4':
            if ENEMY_DATA['o5']['defeated']:
                ENEMY_DATA['m4']['complete'] = True

        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]

        if sprites and not self.battle:
            self.transition_target = sprites[0].target
            self.transition_mermaid = self.transition_target[2]
            if ENEMY_DATA[self.transition_mermaid]['complete']:
                self.player.block()
                self.tint_mode = 'tint'

    def tint_screen(self, dt):
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                if type(self.transition_target) == Battle:
                    self.battle = self.transition_target
                elif self.transition_target == 'level':
                    self.battle = None
                else:
                    self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
                # ^^^ since the target is a tuple of the map then the players starting position
                self.transition_target = None
                self.tint_mode = 'untint'

        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt

        self.tint_progress = max(0, min(self.tint_progress, 255))  # prevents waiting times, tint progress is fixed between 0 and 255
        self.tint_surf.set_alpha(self.tint_progress) # set alpha makes value go from 0 to 255 at the moment of tint progress
        self.display_surface.blit(self.tint_surf, (0, 0))

    # currency system
    def draw_gold(self, gold):
        gold_surf = self.fonts['regular2'].render(str(gold), False, 'white')
        gold_rect = gold_surf.get_frect(bottomleft=(10, 710))
        self.display_surface.blit(gold_surf, gold_rect)

    def stat_changes(self):
        # stat changes based on changes made to equipped items
        if self.equipped_armour == 'Leather Armour':
            if PLAYER_DATA['stats']['HP'] == PLAYER_DATA['max_stats']['HP']:
                PLAYER_DATA['max_stats']['HP'] = 70
                PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
                PLAYER_DATA['stats']['DF'] = 8
            PLAYER_DATA['max_stats']['HP'] = 70
            PLAYER_DATA['stats']['DF'] = 8
        if self.equipped_armour == 'Metal Armour':
            if PLAYER_DATA['stats']['HP'] == PLAYER_DATA['max_stats']['HP']:
                PLAYER_DATA['max_stats']['HP'] = 100
                PLAYER_DATA['stats']['HP'] = PLAYER_DATA['max_stats']['HP']
            PLAYER_DATA['max_stats']['HP'] = 100
            PLAYER_DATA['stats']['DF'] = 15
        if self.equipped_weapon == 'Cutlass':
            PLAYER_DATA['stats']['AT'] = 20
        if self.equipped_weapon == 'Cannon Balls':
            PLAYER_DATA['stats']['AT'] = 40
        if self.equipped_weapon == 'Dagger':
            PLAYER_DATA['stats']['AT'] = 10

    def load_account_data(self):
        ENEMY_DATA['m1']['complete'] = check_m1_complete(self.accountDetails[0])
        ENEMY_DATA['m2']['complete'] = check_m2_complete(self.accountDetails[0])
        ENEMY_DATA['m3']['complete'] = check_m3_complete(self.accountDetails[0])
        ENEMY_DATA['m4']['complete'] = check_m4_complete(self.accountDetails[0])
        ENEMY_DATA['c1']['looted_chest'] = check_c1_looted(self.accountDetails[0])
        ENEMY_DATA['c2']['looted_chest'] = check_c2_looted(self.accountDetails[0])
        ENEMY_DATA['c3']['looted_chest'] = check_c3_looted(self.accountDetails[0])
        ENEMY_DATA['c4']['looted_chest'] = check_c4_looted(self.accountDetails[0])
        ENEMY_DATA['c5']['looted_chest'] = check_c5_looted(self.accountDetails[0])
        ENEMY_DATA['c6']['looted_chest'] = check_c6_looted(self.accountDetails[0])
        ENEMY_DATA['c7']['looted_chest'] = check_c7_looted(self.accountDetails[0])
        ENEMY_DATA['b1']['looted_barrel'] = check_b1_looted(self.accountDetails[0])
        ENEMY_DATA['b2']['looted_barrel'] = check_b2_looted(self.accountDetails[0])
        ENEMY_DATA['b3']['looted_barrel'] = check_b3_looted(self.accountDetails[0])
        ENEMY_DATA['b4']['looted_barrel'] = check_b4_looted(self.accountDetails[0])
        ENEMY_DATA['b5']['looted_barrel'] = check_b5_looted(self.accountDetails[0])
        ENEMY_DATA['b6']['looted_barrel'] = check_b6_looted(self.accountDetails[0])
        ENEMY_DATA['o1']['defeated'] = check_o1_defeated(self.accountDetails[0])
        ENEMY_DATA['o2']['defeated'] = check_o2_defeated(self.accountDetails[0])
        ENEMY_DATA['o3']['defeated'] = check_o3_defeated(self.accountDetails[0])
        ENEMY_DATA['o4']['defeated'] = check_o4_defeated(self.accountDetails[0])
        ENEMY_DATA['o5']['defeated'] = check_o5_defeated(self.accountDetails[0])
        ENEMY_DATA['o1']['killed'] = check_o1_killed(self.accountDetails[0])
        ENEMY_DATA['o2']['killed'] = check_o2_killed(self.accountDetails[0])
        ENEMY_DATA['o3']['killed'] = check_o2_killed(self.accountDetails[0])
        ENEMY_DATA['o4']['killed'] = check_o4_killed(self.accountDetails[0])
        ENEMY_DATA['o5']['killed'] = check_o5_killed(self.accountDetails[0])
        ENEMY_DATA['o1']['spared'] = check_o1_spared(self.accountDetails[0])
        ENEMY_DATA['o2']['spared'] = check_o2_spared(self.accountDetails[0])
        ENEMY_DATA['o3']['spared'] = check_o3_spared(self.accountDetails[0])
        ENEMY_DATA['o4']['spared'] = check_o4_spared(self.accountDetails[0])
        ENEMY_DATA['o5']['spared'] = check_o5_spared(self.accountDetails[0])
        PLAYER_DATA['stats']['HP'] = check_HP(self.accountDetails[0])
        PLAYER_DATA['stats']['AT'] = check_AT(self.accountDetails[0])
        PLAYER_DATA['stats']['DF'] = check_DF(self.accountDetails[0])
        PLAYER_DATA['stats']['SPEED'] = check_SPEED(self.accountDetails[0])
        PLAYER_DATA['stats']['EXP'] = check_EXP(self.accountDetails[0])
        PLAYER_DATA['max_stats']['HP'] = check_maxHP(self.accountDetails[0])
        self.damage = check_damage(self.accountDetails[0])
        self.gold = check_gold(self.accountDetails[0])

    # run everything
    def run(self):
        while True:
            dt = self.clock.tick() / 1000  # delta time is the clocks fastest fps divided by 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # update
            self.input()
            self.transition_check()
            self.all_sprites.update(dt)  # pass delta time as argument for update method so it can be used in move method
            self.stat_changes()

            # drawing
            self.display_surface.fill('#8e8bb7')
            self.all_sprites.draw(self.player.rect.center)  # update sprites on display surface
            self.draw_gold(self.gold)

            # overlays
            if self.dialog_tree:     self.dialog_tree.update()  # if dialog tree is true then use its update method
            if self.index_open:      self.monster_index.update(dt)
            if self.inventory_open:  self.inventory.update()
            if self.menu_open:       self.mini_menu.update(dt)
            if self.stats_menu_open: self.stats_menu.update()
            if self.battle: self.battle.update(dt)

            self.tint_screen(dt)
            pygame.display.update()


initial_menu()
