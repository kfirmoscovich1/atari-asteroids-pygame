"""
Main menu module for the Asteroids game.
This module contains the main menu interface and handles the intro video playback
when the game first starts.
"""
import pygame
import sys
import os
from pathlib import Path
from logic.Game import run_game
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
    FONT_PATH, TITLE_FONT_SIZE, OPTION_FONT_SIZE,
    SMALL_FONT_SIZE, FPS
)
from utils.Resource_Loader import load_image, load_font, get_asset_path

# Global variable to identify if the video has already been played
intro_played = False

# Try to import cv2 (OpenCV) for video playback - works better with PyInstaller
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[INFO] OpenCV not installed - intro video will be skipped")


def play_intro_video(screen):
    """
    Play the Atari intro video at the start of the game.

    This function plays a retro-style intro video when the game is first launched.
    The video loops twice and can be skipped with any key press.
    Uses OpenCV (cv2) for video playback as it works reliably with PyInstaller.

    Args:
        screen: Pygame surface to draw the video on
    """
    if not CV2_AVAILABLE:
        print("[INFO] OpenCV not available, skipping intro video")
        return
        
    video_path = get_asset_path('assets/atari.mp4')
    print(f"[DEBUG] Looking for video at: {video_path}")
    if not video_path.exists():
        print("[INFO] Intro video not found, skipping...")
        return

    print("[INFO] Playing intro video...")
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print("[ERROR] Could not open video file")
            return

        clock = pygame.time.Clock()
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        
        # Calculate target size (half screen size)
        target_width = SCREEN_WIDTH // 2
        target_height = SCREEN_HEIGHT // 2

        loop_count = 0
        
        # Play the video twice unless interrupted
        while loop_count < 2:
            ret, frame = cap.read()
            
            # Reset video when it ends
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                loop_count += 1
                continue

            # Check for exit or skip events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    cap.release()
                    return  # Skip video when any key is pressed

            # Convert BGR (OpenCV) to RGB and then to pygame surface
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (target_width, target_height))
            
            # Rotate and flip for correct pygame orientation
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            
            frame_surface = pygame.surfarray.make_surface(frame)

            screen.fill(BLACK)
            screen.blit(frame_surface, frame_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            pygame.display.update()
            clock.tick(fps)

        cap.release()

        # Brief pause after video ends
        pause_start = pygame.time.get_ticks()
        while (pygame.time.get_ticks() - pause_start) < 100:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            pygame.display.update()
            clock.tick(60)
    except Exception as e:
        print(f"Error playing intro video: {e}")


def Menu():
    """
    Display the main menu with options to start game, view instructions, or quit.

    This function creates the main menu interface that serves as the entry point
    for the player. It handles navigation to other screens and the intro video playback
    on first launch.
    """
    from ui.Instructions import Instructions
    global intro_played

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Menu")
    clock = pygame.time.Clock()

    title_font = load_font(FONT_PATH, TITLE_FONT_SIZE)
    option_font = load_font(FONT_PATH, OPTION_FONT_SIZE)
    small_font = load_font(FONT_PATH, SMALL_FONT_SIZE)

    # Play intro video only on first launch
    if not intro_played:
        play_intro_video(screen)
        intro_played = True

    # Load keyboard key images
    key_images = {
        "ENTER": load_image("assets/keys/enter.png"),
        "SHIFT": load_image("assets/keys/shift.png"),
        "ESC": load_image("assets/keys/esc.png")
    }

    # Scale images to consistent height
    key_target_height = 48
    for key in key_images:
        if key_images[key]:
            img = key_images[key]
            aspect_ratio = img.get_width() / img.get_height()
            new_width = int(aspect_ratio * key_target_height)
            key_images[key] = pygame.transform.scale(img, (new_width, key_target_height))

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run_game()  # Start the game
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    Instructions()  # Show instructions screen
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Exit the game
                    sys.exit()

        # Title text
        title_text = title_font.render("ASTEROIDS", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        # Check if all key images were loaded successfully
        if all(key in key_images and key_images[key] for key in ["ENTER", "SHIFT", "ESC"]):
            # "Press [ENTER] to Start" line
            press_text = option_font.render("Press", True, WHITE)
            to_start_text = option_font.render("to Start", True, WHITE)

            # Calculate layout for centered alignment
            total_width = press_text.get_width() + 10 + key_images["ENTER"].get_width() + 10 + to_start_text.get_width()
            start_x = (SCREEN_WIDTH - total_width) // 2
            y = SCREEN_HEIGHT // 2

            # Render the "Press ENTER to Start" line
            screen.blit(press_text, (start_x, y - press_text.get_height() // 2))
            enter_x = start_x + press_text.get_width() + 10
            screen.blit(key_images["ENTER"], (enter_x, y - key_images["ENTER"].get_height() // 2))
            screen.blit(to_start_text, (enter_x + key_images["ENTER"].get_width() + 10, y - to_start_text.get_height() // 2))

            # Bottom line: "Press [SHIFT] for Instructions | Press [ESC] to Quit"
            press_text2 = small_font.render("Press ", True, WHITE)
            for_instructions_text = small_font.render(" for Instructions | Press ", True, WHITE)
            to_quit_text = small_font.render(" to Quit", True, WHITE)

            # Calculate layout for centered alignment of bottom text
            total_width_bottom = (
                press_text2.get_width() + 5 +
                key_images["SHIFT"].get_width() + 5 +
                for_instructions_text.get_width() + 5 +
                key_images["ESC"].get_width() + 5 +
                to_quit_text.get_width()
            )
            bottom_start_x = (SCREEN_WIDTH - total_width_bottom) // 2
            bottom_y = SCREEN_HEIGHT - 40

            # Render the bottom instruction line
            screen.blit(press_text2, (bottom_start_x, bottom_y - press_text2.get_height() // 2))
            shift_x = bottom_start_x + press_text2.get_width() + 5
            screen.blit(key_images["SHIFT"], (shift_x, bottom_y - key_images["SHIFT"].get_height() // 2))
            after_shift_x = shift_x + key_images["SHIFT"].get_width() + 5
            screen.blit(for_instructions_text, (after_shift_x, bottom_y - for_instructions_text.get_height() // 2))
            esc_x = after_shift_x + for_instructions_text.get_width() + 5
            screen.blit(key_images["ESC"], (esc_x, bottom_y - key_images["ESC"].get_height() // 2))
            after_esc_x = esc_x + key_images["ESC"].get_width() + 5
            screen.blit(to_quit_text, (after_esc_x, bottom_y - to_quit_text.get_height() // 2))
        else:
            # Fallback for when images can't be loaded
            start_text = option_font.render("Press ENTER to Start", True, WHITE)
            inst_text = option_font.render("Press SHIFT for Instructions", True, WHITE)
            quit_text = option_font.render("Press ESC to Quit", True, WHITE)

            screen.blit(start_text, start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(inst_text, inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        pygame.display.update()
        clock.tick(FPS)