"""
Resource loading utility module for the Asteroids game.
This module contains functions for loading game resources like images,
sounds, and fonts with proper error handling and cross-platform path resolution.
"""
from pathlib import Path
from typing import Optional
import pygame
import sys
import os

# Get the project root directory
# Support both normal execution and PyInstaller bundled execution
if getattr(sys, 'frozen', False):
    # Running as compiled EXE (PyInstaller)
    _PROJECT_ROOT = Path(sys._MEIPASS)
else:
    # Running as script
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_asset_path(relative_path: str) -> Path:
    """
    Convert a relative asset path to an absolute path from project root.

    This ensures assets can be loaded regardless of the current working directory,
    which is essential for running the game from different locations.
    Also supports PyInstaller bundled executables.

    Args:
        relative_path: Path relative to the project root (e.g., 'assets/sounds/fire.wav')

    Returns:
        Path: Absolute path to the asset
    """
    return _PROJECT_ROOT / relative_path


def load_image(path: str) -> Optional[pygame.Surface]:
    """
    Load an image from the specified path with alpha channel support.

    This function loads an image and converts it to a format optimized for
    alpha transparency, which is important for images that need transparent
    backgrounds like sprites.

    Args:
        path: Path to the image file (relative to project root or absolute)

    Returns:
        The loaded image surface, or None if loading failed
    """
    try:
        # Convert relative paths to absolute paths from project root
        asset_path = get_asset_path(path) if not Path(path).is_absolute() else Path(path)
        
        if not asset_path.exists():
            print(f"[ERROR] Image not found: {asset_path}")
            print(f"  Hint: Make sure the file exists in the assets directory.")
            return None
            
        image = pygame.image.load(str(asset_path)).convert_alpha()
        return image
    except pygame.error as e:
        print(f"[ERROR] Unable to load image {path}: {e}")
        return None


def load_sound(path: str) -> Optional[pygame.mixer.Sound]:
    """
    Load a sound effect from the specified path.

    This function attempts to load a sound file but returns None instead
    of exiting if the sound cannot be loaded. This allows the game to continue
    without sound effects if necessary.

    Args:
        path: Path to the sound file (relative to project root or absolute)

    Returns:
        The loaded sound, or None if loading failed
    """
    try:
        # Convert relative paths to absolute paths from project root
        asset_path = get_asset_path(path) if not Path(path).is_absolute() else Path(path)
        
        if not asset_path.exists():
            print(f"[WARNING] Sound not found: {asset_path}")
            return None
            
        sound = pygame.mixer.Sound(str(asset_path))
        return sound
    except pygame.error as e:
        print(f"[WARNING] Unable to load sound {path}: {e}")
        return None


def load_font(path: str, size: int) -> pygame.font.Font:
    """
    Load a font from the specified path with the given size.

    This function loads a font file for text rendering. If the font
    cannot be loaded, it falls back to the default pygame font.

    Args:
        path: Path to the font file (relative to project root or absolute)
        size: Size of the font in points

    Returns:
        The loaded font, or default pygame font as fallback
    """
    try:
        # Convert relative paths to absolute paths from project root
        asset_path = get_asset_path(path) if not Path(path).is_absolute() else Path(path)
        
        if not asset_path.exists():
            print(f"[WARNING] Font not found: {asset_path}, using default font")
            return pygame.font.Font(None, size)
            
        font = pygame.font.Font(str(asset_path), size)
        return font
    except Exception as e:
        print(f"[WARNING] Unable to load font {path}: {e}, using default font")
        return pygame.font.Font(None, size)