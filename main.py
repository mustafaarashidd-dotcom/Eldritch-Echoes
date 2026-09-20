import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Combat Index Example")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Combat index setup
combat_index = -1
print("Dialog")
combat_index += 1  # Sets combat_index to 0 initially

# Timer setup
delay = 10000  # 10 seconds in milliseconds
start_time = pygame.time.get_ticks()  # Start time for delay

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen to white

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Combat logic
    if combat_index == 0:
        # Print "Attack!" and display it on the screen
        print("Attack!")
        font = pygame.font.Font(None, 36)
        text = font.render("Attack!", True, BLACK)
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))

        # Check if 10 seconds have passed
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= delay:
            combat_index += 1  # Increment combat_index after 10 seconds
            start_time = current_time  # Reset start_time for any further delay

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()