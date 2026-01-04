"""
Game constants and configuration for the Asteroids game.
This module contains all the constant values used throughout the game,
making it easy to adjust game parameters in a central location.

All values are typed for better IDE support and documentation.
"""
from typing import Dict, List, Tuple
import pygame
pygame.init()

# Type aliases for clarity
Color = Tuple[int, int, int]

# =============================================================================
# SCREEN SETTINGS
# =============================================================================
SCREEN_WIDTH: int = 800      # Width of the game window in pixels
SCREEN_HEIGHT: int = 600     # Height of the game window in pixels

# =============================================================================
# GAME SETTINGS
# =============================================================================
FPS: int = 60                # Frames per second (controls game speed)
ASTEROID_SPAWN_INTERVAL: int = 3000  # Time between new asteroid spawns in milliseconds
BULLET_SPEED: int = 10       # Speed multiplier for bullets

# =============================================================================
# SPACESHIP SETTINGS
# =============================================================================
SPACESHIP_ACCELERATION: float = 0.2   # Acceleration rate of the spaceship
SPACESHIP_FRICTION: float = 0.99      # Friction coefficient (values closer to 1 mean less friction)
SPACESHIP_ROTATION_SPEED: int = 5     # Rotation speed in degrees per frame
SPACESHIP_RADIUS: int = 15            # Collision radius of the spaceship

# =============================================================================
# ASTEROID SETTINGS
# =============================================================================
MIN_VERTICES: int = 6        # Minimum number of vertices for asteroid polygons
MAX_VERTICES: int = 10       # Maximum number of vertices for asteroid polygons
MIN_RADIUS_FACTOR: int = 8   # Minimum radius multiplier for asteroid size
MAX_RADIUS_FACTOR: int = 12  # Maximum radius multiplier for asteroid size
ASTEROID_MIN_SPEED: int = -2 # Minimum speed component (negative allows reverse direction)
ASTEROID_MAX_SPEED: int = 2  # Maximum speed component
ASTEROID_SIZES: List[int] = [1, 2, 3]  # Available asteroid size categories
ASTEROID_SCORE: Dict[int, int] = {
    1: 100,  # Small asteroid (highest points - hardest to hit, like original 1979)
    2: 50,   # Medium asteroid
    3: 20    # Large asteroid (lowest points - easiest to hit)
}

# =============================================================================
# COLORS (RGB tuples)
# =============================================================================
WHITE: Color = (255, 255, 255)   # Used for: Spaceship, Bullet
YELLOW: Color = (255, 255, 0)    # Used for: Asteroid color option
PINK: Color = (255, 105, 180)    # Used for: Asteroid color option
ORANGE: Color = (255, 165, 0)    # Used for: Asteroid color option
PURPLE: Color = (138, 43, 226)   # Used for: Asteroid color option
BLACK: Color = (0, 0, 0)         # Used for: Background

# =============================================================================
# FONT SIZES (in points)
# =============================================================================
TITLE_FONT_SIZE: int = 76      # Size for main titles
OPTION_FONT_SIZE: int = 26     # Size for menu options
SMALL_FONT_SIZE: int = 20      # Size for smaller text
INPUT_FONT_SIZE: int = 36      # Size for input fields
PAUSE_FONT_SIZE: int = 48      # Size for pause screen text
SCORE_FONT_SIZE: int = 30      # Size for score display

# =============================================================================
# PLAYER SETTINGS
# =============================================================================
INITIAL_LIVES: int = 3         # Number of lives at game start
RESPAWN_DELAY: int = 2000      # Milliseconds of invulnerability after respawn
HYPERSPACE_COOLDOWN: int = 3000  # Milliseconds between hyperspace jumps

# =============================================================================
# UFO SETTINGS
# =============================================================================
UFO_SPAWN_INTERVAL: int = 15000    # Milliseconds between UFO spawn attempts
UFO_SPAWN_CHANCE: float = 0.5      # Probability of UFO spawning when timer fires
UFO_SPEED: float = 2.0             # UFO movement speed
UFO_SHOOT_INTERVAL: int = 2000     # Milliseconds between UFO shots
UFO_SMALL_SCORE: int = 1000        # Points for destroying small UFO
UFO_LARGE_SCORE: int = 200         # Points for destroying large UFO
UFO_SMALL_SIZE: int = 15           # Radius of small UFO
UFO_LARGE_SIZE: int = 25           # Radius of large UFO

# =============================================================================
# SOUND SETTINGS
# =============================================================================
BEAT_INTERVAL_START: int = 1000    # Starting interval between beats (ms)
BEAT_INTERVAL_MIN: int = 200       # Minimum interval between beats (ms)
BEAT_SPEEDUP_RATE: float = 0.95    # Beat interval multiplier per asteroid destroyed

# =============================================================================
# ASSET PATHS (relative to project root)
# =============================================================================
FONT_PATH: str = "assets/fonts/Hyperspace-JvEM.ttf"  # Path to main game font
FIRE_SOUND_PATH: str = "assets/sounds/fire.wav"      # Path to bullet firing sound
BEAT1_SOUND_PATH: str = "assets/sounds/beat1.wav"    # Path to beat1 sound
BEAT2_SOUND_PATH: str = "assets/sounds/beat2.wav"    # Path to beat2 sound
ALT_KEY_IMAGE_PATH: str = "assets/keys/alt.png"      # Path to ALT key image

# =============================================================================
# EXPORTS
# =============================================================================
__all__ = [
    # Screen
    "SCREEN_WIDTH", "SCREEN_HEIGHT",
    # Game
    "FPS", "ASTEROID_SPAWN_INTERVAL", "BULLET_SPEED",
    # Spaceship
    "SPACESHIP_ACCELERATION", "SPACESHIP_FRICTION", 
    "SPACESHIP_ROTATION_SPEED", "SPACESHIP_RADIUS",
    # Player
    "INITIAL_LIVES", "RESPAWN_DELAY", "HYPERSPACE_COOLDOWN",
    # UFO
    "UFO_SPAWN_INTERVAL", "UFO_SPAWN_CHANCE", "UFO_SPEED", "UFO_SHOOT_INTERVAL",
    "UFO_SMALL_SCORE", "UFO_LARGE_SCORE", "UFO_SMALL_SIZE", "UFO_LARGE_SIZE",
    # Sound
    "BEAT_INTERVAL_START", "BEAT_INTERVAL_MIN", "BEAT_SPEEDUP_RATE",
    # Asteroid
    "MIN_VERTICES", "MAX_VERTICES", "MIN_RADIUS_FACTOR", "MAX_RADIUS_FACTOR",
    "ASTEROID_MIN_SPEED", "ASTEROID_MAX_SPEED", "ASTEROID_SIZES", "ASTEROID_SCORE",
    # Colors
    "WHITE", "YELLOW", "PINK", "ORANGE", "PURPLE", "BLACK",
    # Fonts
    "TITLE_FONT_SIZE", "OPTION_FONT_SIZE", "SMALL_FONT_SIZE",
    "INPUT_FONT_SIZE", "PAUSE_FONT_SIZE", "SCORE_FONT_SIZE",
    # Assets
    "FONT_PATH", "FIRE_SOUND_PATH", "BEAT1_SOUND_PATH", "BEAT2_SOUND_PATH", "ALT_KEY_IMAGE_PATH",
]