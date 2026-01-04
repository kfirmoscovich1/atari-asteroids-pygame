"""
UFO (Flying Saucer) class implementation for the Asteroids game.
This module contains the UFO enemy that appears periodically and shoots at the player.
Based on the original 1979 Atari Asteroids game.
"""
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, Optional

import pygame

from logic.Bullet import Bullet
from logic.GameObject import GameObject
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE,
    UFO_SPEED, UFO_SHOOT_INTERVAL,
    UFO_SMALL_SCORE, UFO_LARGE_SCORE,
    UFO_SMALL_SIZE, UFO_LARGE_SIZE
)

if TYPE_CHECKING:
    from logic.Spaceship import Spaceship


class UFO(GameObject):
    """
    UFO (Flying Saucer) enemy class.
    
    UFOs appear from the edges of the screen and move horizontally,
    occasionally changing vertical direction. They shoot at the player
    and are worth bonus points when destroyed.
    
    There are two types:
    - Large UFO: Easier to hit, shoots randomly, worth fewer points
    - Small UFO: Harder to hit, aims at player, worth more points
    
    Attributes:
        x: Horizontal position
        y: Vertical position
        is_small: True if this is a small (harder) UFO
        direction: 1 for moving right, -1 for moving left
        velocity_y: Vertical velocity component
        last_shot_time: Time of last shot fired
        radius: Collision radius
    """
    
    def __init__(self, score: int = 0) -> None:
        """
        Initialize a new UFO.
        
        Args:
            score: Current player score (affects whether UFO is small or large)
        """
        # Higher score = more likely to get small UFO
        small_chance = min(0.7, score / 40000)
        self.is_small: bool = random.random() < small_chance
        self.radius: int = UFO_SMALL_SIZE if self.is_small else UFO_LARGE_SIZE
        self.alive: bool = True
        
        # Spawn from left or right edge
        self.direction: int = random.choice([-1, 1])
        if self.direction == 1:
            self.x: float = -self.radius
        else:
            self.x = SCREEN_WIDTH + self.radius
            
        # Random vertical position
        self.y: float = random.randint(50, SCREEN_HEIGHT - 50)
        self.velocity_y: float = 0
        
        # Shooting timer
        self.last_shot_time: int = pygame.time.get_ticks()
        
        # Direction change timer
        self.last_direction_change: int = pygame.time.get_ticks()
        
    def update(self, delta_time: float = 1.0) -> None:
        """
        Update the UFO's position.
        
        Args:
            delta_time: Time multiplier for frame-independent movement
        """
        # Move horizontally
        self.x += UFO_SPEED * self.direction * delta_time
        
        # Move vertically
        self.y += self.velocity_y * delta_time
        
        # Occasionally change vertical direction
        current_time = pygame.time.get_ticks()
        if current_time - self.last_direction_change > 1000:
            if random.random() < 0.3:
                self.velocity_y = random.uniform(-1.5, 1.5)
                self.last_direction_change = current_time
        
        # Keep within vertical bounds
        if self.y < 30:
            self.y = 30
            self.velocity_y = abs(self.velocity_y)
        elif self.y > SCREEN_HEIGHT - 30:
            self.y = SCREEN_HEIGHT - 30
            self.velocity_y = -abs(self.velocity_y)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the UFO as a classic flying saucer shape.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw classic saucer shape
        # Main body (ellipse)
        body_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius // 3,
            self.radius * 2,
            self.radius * 2 // 3
        )
        pygame.draw.ellipse(screen, WHITE, body_rect, 2)
        
        # Top dome
        dome_rect = pygame.Rect(
            self.x - self.radius // 2,
            self.y - self.radius // 2 - self.radius // 4,
            self.radius,
            self.radius // 2
        )
        pygame.draw.ellipse(screen, WHITE, dome_rect, 2)
        
    def is_on_screen(self) -> bool:
        """
        Check if the UFO is still on screen.
        
        Returns:
            True if UFO is visible, False if it has left the screen
        """
        return -self.radius * 2 <= self.x <= SCREEN_WIDTH + self.radius * 2
    
    def can_shoot(self) -> bool:
        """
        Check if enough time has passed to shoot again.
        
        Returns:
            True if UFO can fire a new bullet
        """
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= UFO_SHOOT_INTERVAL
    
    def shoot(self, spaceship: Optional[Spaceship] = None) -> Bullet:
        """
        Fire a bullet, optionally aimed at the player.
        
        Args:
            spaceship: If provided and this is a small UFO, aim at it
            
        Returns:
            A new Bullet instance
        """
        self.last_shot_time = pygame.time.get_ticks()
        
        if self.is_small and spaceship:
            # Small UFO aims at player with some accuracy
            dx = spaceship.x - self.x
            dy = spaceship.y - self.y
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                # Add some inaccuracy
                accuracy = 0.9  # 90% accurate
                dx = dx / distance + random.uniform(-0.1, 0.1) * (1 - accuracy)
                dy = dy / distance + random.uniform(-0.1, 0.1) * (1 - accuracy)
                
                # Normalize
                length = math.hypot(dx, dy)
                dx /= length
                dy /= length
            else:
                dx, dy = 1, 0
        else:
            # Large UFO shoots randomly
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)
        
        return Bullet(self.x, self.y, dx, dy)
    
    def get_score(self) -> int:
        """
        Get the score value for destroying this UFO.
        
        Returns:
            Point value based on UFO size
        """
        return UFO_SMALL_SCORE if self.is_small else UFO_LARGE_SCORE
    
    def get_radius(self) -> float:
        """
        Get the collision radius.
        
        Returns:
            Collision radius for hit detection
        """
        return float(self.radius)
    
    @staticmethod
    def should_spawn(player_score: int) -> bool:
        """
        Determine if a UFO should spawn.
        
        Args:
            player_score: Current player score
            
        Returns:
            True if a UFO should spawn
        """
        # UFOs start spawning after reaching some score
        if player_score < 1000:
            return False
        return True
