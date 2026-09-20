# Importing statements
from button_old import *
import time
from AccountDatabase import *
import MainMenu
import sys
from settings_old import *
from level_old import Level  # Import level class
# Pygame imported from other imports like button page

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
font3 = pygame.font.SysFont("Callibri", 55)  # 3rd font defined
TEXT_COL2 = "lightGrey"
font4 = pygame.font.SysFont("arialblack", 20)
TEXT_COL3 = "Red"
TEXT_COL4 = "Green"
font5 = pygame.font.SysFont("arialblack", 90)
font6 = pygame.font.SysFont("Callibri", 165)
TEXT_COL5 = (86, 208, 216)
font7 = pygame.font.SysFont("arialblack", 30)

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
                    print("Leaderboard")
                if SETTINGS_BUTTON.checkForInput(MainMenu_mouse_pos):
                    # settings()
                    print("Settings")
                if TUTORIAL_BUTTON.checkForInput(MainMenu_mouse_pos):
                    # tutorial()
                    print("Tutorial")
                if MAIN_MENU_BACK.checkForInput(MainMenu_mouse_pos):
                    main_menu_music.stop()
                    mainMenu_music_playing = False
                    login()

        pygame.display.update()
        clock.tick(FPS)

class Game:  # Create the main game class
    def __init__(self):  # Create attributes

        # general setup
        pygame.init()  # initialize pygame
        self.screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))  # Create game window
        self.clock = pygame.time.Clock()  # Create game clock

        self.level = Level()

    def run(self):  # Run method for the game
        while True:  # main game loop
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If exiting quit pygame and break the loop
                    pygame.quit()
                    sys.exit()
                # BACK TO MAIN MENU TESTER:
                #if event.type == pygame.MOUSEBUTTONDOWN and pygame.collidepoint(menubutton):
                #    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Re initialize screen
                #    # or the width and height remain the same upon leaving to main menu
                #    main_menu()
                # ------------------------------------------------------------------------------------------------

            self.screen.fill('black')  # fill screen with colour black before updating
            self.level.run()  # Runs level class 'run' method
            pygame.display.update()  # Update screen
            self.clock.tick(FPS)  # Run game clock at FPS (=60)


initial_menu()
