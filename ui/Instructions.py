"""
Instructions screen module for the Asteroids game.
This module displays the game controls and commands to help players understand
how to play the game.
"""
import pygame
import sys
from utils.Constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FONT_PATH, TITLE_FONT_SIZE, OPTION_FONT_SIZE, FPS
from utils.Resource_Loader import load_image, load_font

def Instructions():
    """
    Display the instructions screen showing game controls and key mappings.

    This function creates an instructions screen that shows all the keyboard
    controls for playing the game. Each control is visualized with an image
    of the corresponding key paired with a description of its function.
    """
    from ui.Menu import Menu

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Instructions")
    clock = pygame.time.Clock()

    title_font = load_font(FONT_PATH, TITLE_FONT_SIZE)
    text_font = load_font(FONT_PATH, OPTION_FONT_SIZE)

    # Load images of keyboard keys for visual instructions
    key_images = {
        "UP": load_image("assets/keys/up.png"),
        "LEFT": load_image("assets/keys/left.png"),
        "RIGHT": load_image("assets/keys/right.png"),
        "SHIFT": load_image("assets/keys/shift.png"),
        "SPACE": load_image("assets/keys/space.png"),
        "ALT": load_image("assets/keys/alt.png"),
        "S": load_image("assets/keys/s.png"),
        "ESC": load_image("assets/keys/esc.png")
    }

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu()  # Return to main menu when Escape is pressed

        # Title text
        title = title_font.render("INSTRUCTIONS", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 60)))

        # List of key-action pairs to display
        instructions = [
            ("UP",    "MOVE FORWARD"),
            ("LEFT",  "ROTATE LEFT"),
            ("RIGHT", "ROTATE RIGHT"),
            ("SPACE", "SHOOT"),
            ("SHIFT", "HYPERSPACE / INSTRUCTIONS"),
            ("ALT",   "PAUSE / RESUME"),
            ("S",     "SAVE SCORE"),
            ("ESC",   "GO BACK / QUIT GAME"),
        ]

        # Layout parameters for the instruction list
        start_y = 150   # Starting Y position
        space_y = 45    # Vertical spacing between rows
        key_x = 100     # X position for key images
        action_x = 350  # X position for action descriptions
        box_height = 40 # Standard height for key images

        # Draw each instruction row
        for idx, (key, action) in enumerate(instructions):
            y = start_y + idx * space_y

            # Check if the key image exists and is valid
            if key in key_images and key_images[key]:
                # Scale the key image to maintain consistent height
                key_img = key_images[key]
                img_width = key_img.get_width()
                img_height = key_img.get_height()

                scale_factor = box_height / img_height
                new_width = int(img_width * scale_factor)

                key_img = pygame.transform.scale(key_img, (new_width, box_height))
                key_rect = key_img.get_rect(topleft=(key_x, y - box_height // 2))
                screen.blit(key_img, key_rect)
            else:
                # Fallback if image couldn't be loaded
                key_text = text_font.render(key, True, WHITE)
                screen.blit(key_text, key_text.get_rect(left=key_x, centery=y))

            # Draw the action description
            action_text = text_font.render(action, True, WHITE)
            action_rect = action_text.get_rect(left=action_x, centery=y)
            screen.blit(action_text, action_rect)

        pygame.display.update()
        clock.tick(FPS)