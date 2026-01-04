"""
End screen module for the Asteroids game.
This module contains the game over screen that appears when the player is hit by an asteroid,
allowing players to restart, return to menu, or save their score.
"""
import pygame
import sys
from pathlib import Path
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
    FONT_PATH, TITLE_FONT_SIZE, OPTION_FONT_SIZE,
    INPUT_FONT_SIZE, SMALL_FONT_SIZE, FPS
)
from utils.Resource_Loader import load_image, load_font, get_asset_path

# Path for scores file (in project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SCORES_FILE = _PROJECT_ROOT / "scores.txt"

def EndScreen(final_score=0):
    """
    Display the game over screen with score saving functionality.

    This function creates the end game screen that appears when the player loses.
    It offers options to restart, return to the main menu, or save the current score.

    Args:
        final_score (int): The player's final score to display and potentially save
    """
    from ui.Menu import Menu
    from logic.Game import run_game

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")
    clock = pygame.time.Clock()

    title_font = load_font(FONT_PATH, TITLE_FONT_SIZE)
    option_font = load_font(FONT_PATH, OPTION_FONT_SIZE)
    small_font = load_font(FONT_PATH, SMALL_FONT_SIZE)
    input_font = load_font(FONT_PATH, INPUT_FONT_SIZE)

    # Import images for keyboard key visualization
    key_images = {
        "ENTER": load_image("assets/keys/enter.png"),
        "ESC": load_image("assets/keys/esc.png"),
        "S": load_image("assets/keys/s.png")
    }

    # Adjusting the size of images to maintain consistent height
    key_target_height = 48
    for key in key_images:
        if key_images[key]:
            img = key_images[key]
            aspect_ratio = img.get_width() / img.get_height()
            new_width = int(aspect_ratio * key_target_height)
            key_images[key] = pygame.transform.scale(img, (new_width, key_target_height))

    saving_score = False  # Flag to track if in score saving mode
    name_input = ""       # Player name for score saving

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if saving_score:
                    # Handle text input when saving score
                    if event.key == pygame.K_RETURN:
                        save_score(name_input, final_score)
                        Menu()
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]  # Remove last character
                    else:
                        if len(name_input) < 12:  # Limit name length
                            name_input += event.unicode
                else:
                    # Handle standard end screen navigation
                    if event.key == pygame.K_RETURN:
                        run_game()  # Restart the game
                    elif event.key == pygame.K_ESCAPE:
                        Menu()  # Return to main menu
                    elif event.key == pygame.K_s:
                        saving_score = True  # Enter score saving mode

        # Game Over text
        title = title_font.render("GAME OVER", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        if saving_score:
            # Display name input field in save score mode
            enter_name = input_font.render("Enter Your Name: " + name_input, True, WHITE)
            screen.blit(enter_name, enter_name.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            if key_images and key_images["ENTER"]:
                # Show Enter key instruction for saving
                press_text = small_font.render("Press ", True, WHITE)
                to_save_text = small_font.render(" to Save", True, WHITE)

                total_width = press_text.get_width() + 5 + key_images["ENTER"].get_width() + 5 + to_save_text.get_width()
                start_x = (SCREEN_WIDTH - total_width) // 2
                bottom_y = SCREEN_HEIGHT - 30

                screen.blit(press_text, (start_x, bottom_y - press_text.get_height() // 2))

                enter_x = start_x + press_text.get_width() + 5
                screen.blit(key_images["ENTER"], (enter_x, bottom_y - key_images["ENTER"].get_height() // 2))

                after_enter_x = enter_x + key_images["ENTER"].get_width() + 5
                screen.blit(to_save_text, (after_enter_x, bottom_y - to_save_text.get_height() // 2))

        else:
            # Normal mode: Displays save instructions + Restart / Menu options
            if key_images and all(k in key_images and key_images[k] for k in ["S", "ENTER", "ESC"]):
                # "Press [S] to Save Your Score" line
                press_text = option_font.render("Press ", True, WHITE)
                for_save_text = option_font.render(" to Save Your Score", True, WHITE)

                total_width = press_text.get_width() + 5 + key_images["S"].get_width() + 5 + for_save_text.get_width()
                start_x = (SCREEN_WIDTH - total_width) // 2
                center_y = SCREEN_HEIGHT // 2

                screen.blit(press_text, (start_x, center_y - press_text.get_height() // 2))

                s_x = start_x + press_text.get_width() + 5
                screen.blit(key_images["S"], (s_x, center_y - key_images["S"].get_height() // 2))

                screen.blit(for_save_text, (s_x + key_images["S"].get_width() + 5, center_y - for_save_text.get_height() // 2))

                # Bottom line: "Press [ENTER] to Restart | Press [ESC] to Menu"
                press_enter_text = small_font.render("Press ", True, WHITE)
                to_restart_text = small_font.render(" to Restart | Press ", True, WHITE)
                to_menu_text = small_font.render(" to Menu", True, WHITE)

                total_width_bottom = (
                    press_enter_text.get_width() + 5 +
                    key_images["ENTER"].get_width() + 5 +
                    to_restart_text.get_width() + 5 +
                    key_images["ESC"].get_width() + 5 +
                    to_menu_text.get_width()
                )
                bottom_start_x = (SCREEN_WIDTH - total_width_bottom) // 2
                bottom_y = SCREEN_HEIGHT - 30

                screen.blit(press_enter_text, (bottom_start_x, bottom_y - press_enter_text.get_height() // 2))

                enter_x = bottom_start_x + press_enter_text.get_width() + 5
                screen.blit(key_images["ENTER"], (enter_x, bottom_y - key_images["ENTER"].get_height() // 2))

                after_enter_x = enter_x + key_images["ENTER"].get_width() + 5
                screen.blit(to_restart_text, (after_enter_x, bottom_y - to_restart_text.get_height() // 2))

                esc_x = after_enter_x + to_restart_text.get_width() + 5
                screen.blit(key_images["ESC"], (esc_x, bottom_y - key_images["ESC"].get_height() // 2))

                after_esc_x = esc_x + key_images["ESC"].get_width() + 5
                screen.blit(to_menu_text, (after_esc_x, bottom_y - to_menu_text.get_height() // 2))

        pygame.display.update()
        clock.tick(FPS)

def save_score(name: str, score: int) -> None:
    """
    Save the player's name and score to a text file.

    Args:
        name: Player's name
        score: Player's final score
    """
    try:
        with open(_SCORES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{name} - {score}\n")
        print(f"[INFO] Score saved: {name} - {score}")
    except Exception as e:
        print(f"[ERROR] Failed to save score: {e}")