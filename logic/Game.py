"""
Main game module for the Asteroids game.
This module contains the core game loop and handles game state, collisions, 
rendering, and user input for the main gameplay experience.

Features faithful to the original 1979 Atari Asteroids:
- 3 lives system with respawn invulnerability
- UFO enemies (large and small) that shoot at the player
- Hyperspace teleportation (risky escape move)
- Alternating beat sounds that speed up as score increases
- Delta-time physics for consistent gameplay across frame rates
"""
from typing import List, Optional, Tuple

import pygame
import sys

from logic.Spaceship import Spaceship
from logic.Asteroid import Asteroid
from logic.Bullet import Bullet
from logic.UFO import UFO
from logic.Collision import check_collision
from ui.EndScreen import EndScreen
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE,
    FONT_PATH, SMALL_FONT_SIZE, SCORE_FONT_SIZE,
    PAUSE_FONT_SIZE, FIRE_SOUND_PATH, ALT_KEY_IMAGE_PATH,
    ASTEROID_SPAWN_INTERVAL, INITIAL_LIVES,
    UFO_SPAWN_INTERVAL, UFO_SHOOT_INTERVAL,
    BEAT_INTERVAL_START, BEAT_INTERVAL_MIN, BEAT_SPEEDUP_RATE,
    BEAT1_SOUND_PATH, BEAT2_SOUND_PATH
)
from utils.Resource_Loader import load_image, load_sound, load_font

# Number of asteroids to spawn at game start
INITIAL_ASTEROID_COUNT: int = 5

# Key image target height for pause screen
KEY_IMAGE_HEIGHT: int = 48


def run_game() -> None:
    """
    Main game function that initializes and runs the Asteroids game.

    This function handles:
    - Game initialization (pygame setup, audio, display)
    - Game loop management with delta-time physics
    - User input processing (movement, shooting, hyperspace)
    - Game state updates (player, asteroids, bullets, UFO)
    - Lives system with respawn mechanics
    - Collision detection and response
    - Rendering of all game elements
    - Beat sound system that speeds up with score
    - Pause functionality

    Returns to the menu screen when the game ends.
    """
    # Initialize pygame subsystems
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"[WARNING] Audio mixer initialization failed: {e}")

    # Set up display
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Game")
    clock: pygame.time.Clock = pygame.time.Clock()

    # Load sounds
    fire_sound: Optional[pygame.mixer.Sound] = load_sound(FIRE_SOUND_PATH)
    if fire_sound:
        fire_sound.set_volume(0.5)
    
    # Load beat sounds (original Asteroids heartbeat)
    beat1_sound: Optional[pygame.mixer.Sound] = load_sound(BEAT1_SOUND_PATH)
    beat2_sound: Optional[pygame.mixer.Sound] = load_sound(BEAT2_SOUND_PATH)
    if beat1_sound:
        beat1_sound.set_volume(0.3)
    if beat2_sound:
        beat2_sound.set_volume(0.3)

    # Load key images for pause screen
    alt_key_image: Optional[pygame.Surface] = load_image(ALT_KEY_IMAGE_PATH)
    if alt_key_image:
        aspect_ratio = alt_key_image.get_width() / alt_key_image.get_height()
        new_width = int(aspect_ratio * KEY_IMAGE_HEIGHT)
        alt_key_image = pygame.transform.scale(alt_key_image, (new_width, KEY_IMAGE_HEIGHT))

    # Initialize game objects
    spaceship: Spaceship = Spaceship()
    asteroids: List[Asteroid] = [
        Asteroid.random_spawn() for _ in range(INITIAL_ASTEROID_COUNT)
    ]
    bullets: List[Bullet] = []
    ufo: Optional[UFO] = None
    ufo_bullets: List[Bullet] = []

    # Game state
    is_paused: bool = False
    score: int = 0
    lives: int = INITIAL_LIVES
    respawn_timer: int = 0  # Time when spaceship should respawn
    
    # Beat sound state (iconic Asteroids heartbeat)
    beat_timer: int = pygame.time.get_ticks()
    beat_interval: int = BEAT_INTERVAL_START
    beat_toggle: bool = True  # Alternate between beat1 and beat2
    
    # UFO spawn timer
    ufo_spawn_timer: int = pygame.time.get_ticks() + UFO_SPAWN_INTERVAL
    ufo_shoot_timer: int = 0
    
    # Load fonts
    score_font: pygame.font.Font = load_font(FONT_PATH, SCORE_FONT_SIZE)
    small_font: pygame.font.Font = load_font(FONT_PATH, SMALL_FONT_SIZE)

    # Custom pygame events
    NEW_ASTEROID_EVENT: int = pygame.USEREVENT + 1
    pygame.time.set_timer(NEW_ASTEROID_EVENT, ASTEROID_SPAWN_INTERVAL)

    # Main game loop
    running: bool = True
    while running:
        # Calculate delta time for frame-independent physics
        dt_ms = clock.tick(FPS)
        delta_time: float = dt_ms / (1000 / FPS)  # Normalized to expected frame time
        current_time: int = pygame.time.get_ticks()
        
        # Clear screen when not paused
        if not is_paused:
            screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    EndScreen(score)
                    return  # Exit game loop after end screen
                    
                elif event.key in (pygame.K_LALT, pygame.K_RALT):
                    is_paused = not is_paused
                    
                elif event.key == pygame.K_SPACE and not is_paused and spaceship.alive:
                    bullets.append(spaceship.shoot())
                    if fire_sound:
                        fire_sound.play()
                
                # Hyperspace - risky teleport (SHIFT key like some arcade versions)
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and not is_paused and spaceship.alive:
                    spaceship.hyperspace()

            if event.type == NEW_ASTEROID_EVENT and not is_paused:
                asteroids.append(Asteroid.random_spawn())

        if not is_paused:
            # Handle respawn timer
            if not spaceship.alive and lives > 0:
                if current_time >= respawn_timer:
                    spaceship.respawn()
            
            # Play beat sounds (speeds up as score increases)
            if current_time >= beat_timer:
                if beat_toggle and beat1_sound:
                    beat1_sound.play()
                elif not beat_toggle and beat2_sound:
                    beat2_sound.play()
                beat_toggle = not beat_toggle
                
                # Speed up beat based on score (faster as score increases)
                beat_interval = max(
                    BEAT_INTERVAL_MIN,
                    int(BEAT_INTERVAL_START * (BEAT_SPEEDUP_RATE ** (score // 1000)))
                )
                beat_timer = current_time + beat_interval
            
            # UFO spawning
            if ufo is None and current_time >= ufo_spawn_timer:
                if UFO.should_spawn(score):
                    ufo = UFO(score)
                    ufo_shoot_timer = current_time + UFO_SHOOT_INTERVAL
                ufo_spawn_timer = current_time + UFO_SPAWN_INTERVAL
            
            # UFO shooting
            if ufo is not None and ufo.alive and current_time >= ufo_shoot_timer:
                if spaceship.alive:
                    ufo_bullet = ufo.shoot(spaceship)
                    if ufo_bullet:
                        ufo_bullets.append(ufo_bullet)
                ufo_shoot_timer = current_time + UFO_SHOOT_INTERVAL
            
            # Update game state with delta time
            _update_game_state(spaceship, asteroids, bullets, ufo, ufo_bullets, delta_time)
            
            # Handle collisions and get updated score and lives
            score, lives, respawn_timer, ufo = _handle_collisions(
                spaceship, asteroids, bullets, ufo, ufo_bullets,
                score, lives, respawn_timer, current_time
            )
            
            # Check for game over
            if lives <= 0 and not spaceship.alive:
                EndScreen(score)
                return
            
            # Render game
            _render_game(screen, spaceship, asteroids, bullets, ufo, ufo_bullets,
                        score, lives, score_font)
        else:
            _render_pause_screen(screen, alt_key_image, small_font)

        pygame.display.update()


def _update_game_state(
    spaceship: Spaceship,
    asteroids: List[Asteroid],
    bullets: List[Bullet],
    ufo: Optional[UFO],
    ufo_bullets: List[Bullet],
    delta_time: float
) -> None:
    """Update all game object positions based on input and physics."""
    # Update spaceship based on keyboard input
    if spaceship.alive:
        keys = pygame.key.get_pressed()
        spaceship.update(keys, delta_time)

    # Update asteroids
    for asteroid in asteroids:
        asteroid.update(delta_time)

    # Update bullets and remove off-screen ones
    for bullet in bullets[:]:
        bullet.update(delta_time)
        if not bullet.is_on_screen():
            bullets.remove(bullet)
    
    # Update UFO
    if ufo is not None and ufo.alive:
        ufo.update(delta_time)
        if not ufo.is_on_screen():
            ufo.alive = False
    
    # Update UFO bullets
    for bullet in ufo_bullets[:]:
        bullet.update(delta_time)
        if not bullet.is_on_screen():
            ufo_bullets.remove(bullet)


def _handle_collisions(
    spaceship: Spaceship,
    asteroids: List[Asteroid],
    bullets: List[Bullet],
    ufo: Optional[UFO],
    ufo_bullets: List[Bullet],
    score: int,
    lives: int,
    respawn_timer: int,
    current_time: int
) -> Tuple[int, int, int, Optional[UFO]]:
    """
    Handle all collision detection and response.
    
    Returns:
        Tuple of (updated score, lives, respawn_timer, ufo)
    """
    # Check bullet-asteroid collisions
    for asteroid in asteroids[:]:
        for bullet in bullets[:]:
            if check_collision(asteroid, bullet):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                score += asteroid.get_score()
                
                # Split asteroid into smaller pieces
                split_asteroids = asteroid.split()
                asteroids.extend(split_asteroids)
                break

        # Check spaceship-asteroid collision
        if asteroid in asteroids and spaceship.alive and spaceship.collides_with(asteroid):
            spaceship.alive = False
            lives -= 1
            if lives > 0:
                respawn_timer = current_time + 2000  # 2 second delay before respawn
    
    # Check bullet-UFO collisions
    if ufo is not None and ufo.alive:
        for bullet in bullets[:]:
            distance = ((ufo.x - bullet.x) ** 2 + (ufo.y - bullet.y) ** 2) ** 0.5
            if distance < ufo.get_radius() + bullet.radius:
                bullets.remove(bullet)
                score += ufo.get_score()
                ufo.alive = False
                break
        
        # Check spaceship-UFO collision
        if ufo.alive and spaceship.alive and spaceship.collides_with_ufo(ufo):
            spaceship.alive = False
            lives -= 1
            ufo.alive = False
            if lives > 0:
                respawn_timer = current_time + 2000
    
    # Check UFO bullet-spaceship collisions
    for bullet in ufo_bullets[:]:
        if spaceship.alive and spaceship.hit_by_bullet(bullet):
            ufo_bullets.remove(bullet)
            spaceship.alive = False
            lives -= 1
            if lives > 0:
                respawn_timer = current_time + 2000
            break
        
        # UFO bullets can also destroy asteroids
        for asteroid in asteroids[:]:
            if check_collision(asteroid, bullet):
                if bullet in ufo_bullets:
                    ufo_bullets.remove(bullet)
                if asteroid in asteroids:
                    asteroids.remove(asteroid)
                    split_asteroids = asteroid.split()
                    asteroids.extend(split_asteroids)
                break
    
    # Clean up dead UFO
    if ufo is not None and not ufo.alive:
        ufo = None
            
    return score, lives, respawn_timer, ufo


def _render_game(
    screen: pygame.Surface,
    spaceship: Spaceship,
    asteroids: List[Asteroid],
    bullets: List[Bullet],
    ufo: Optional[UFO],
    ufo_bullets: List[Bullet],
    score: int,
    lives: int,
    score_font: pygame.font.Font
) -> None:
    """Render all game objects and UI elements."""
    # Draw game objects
    if spaceship.alive:
        spaceship.draw(screen)
    
    for asteroid in asteroids:
        asteroid.draw(screen)
        
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw UFO
    if ufo is not None and ufo.alive:
        ufo.draw(screen)
    
    # Draw UFO bullets
    for bullet in ufo_bullets:
        bullet.draw(screen)

    # Draw score
    score_text = score_font.render(f"{score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw lives as small ship icons
    _draw_lives(screen, lives)


def _draw_lives(screen: pygame.Surface, lives: int) -> None:
    """Draw remaining lives as small ship icons in top-right corner."""
    import math
    ship_size = 12
    spacing = 25
    start_x = SCREEN_WIDTH - 30
    y = 30
    
    for i in range(lives):
        x = start_x - (i * spacing)
        # Draw small ship pointing up
        angle = -90  # Facing up
        front = (x + math.cos(math.radians(angle)) * ship_size,
                 y + math.sin(math.radians(angle)) * ship_size)
        left = (x + math.cos(math.radians(angle + 140)) * (ship_size * 0.67),
                y + math.sin(math.radians(angle + 140)) * (ship_size * 0.67))
        right = (x + math.cos(math.radians(angle - 140)) * (ship_size * 0.67),
                 y + math.sin(math.radians(angle - 140)) * (ship_size * 0.67))
        pygame.draw.polygon(screen, WHITE, [front, left, right], 2)


def _render_pause_screen(
    screen: pygame.Surface,
    alt_key_image: Optional[pygame.Surface],
    small_font: pygame.font.Font
) -> None:
    """Render the pause screen overlay."""
    screen.fill(BLACK)

    pause_font = load_font(FONT_PATH, PAUSE_FONT_SIZE)
    pause_text = pause_font.render("PAUSED", True, WHITE)
    screen.blit(
        pause_text,
        pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    )

    if alt_key_image:
        press_text = small_font.render("Press ", True, WHITE)
        resume_text = small_font.render(" to Resume", True, WHITE)

        total_width = (
            press_text.get_width() + 5 +
            alt_key_image.get_width() + 5 +
            resume_text.get_width()
        )
        start_x = (SCREEN_WIDTH - total_width) // 2
        bottom_y = SCREEN_HEIGHT - 40

        screen.blit(press_text, (start_x, bottom_y - press_text.get_height() // 2))
        
        alt_x = start_x + press_text.get_width() + 5
        screen.blit(alt_key_image, (alt_x, bottom_y - alt_key_image.get_height() // 2))
        
        screen.blit(
            resume_text,
            (alt_x + alt_key_image.get_width() + 5, bottom_y - resume_text.get_height() // 2)
        )