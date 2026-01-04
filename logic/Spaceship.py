"""
Spaceship class implementation for the Asteroids game.
This module contains the player-controlled Spaceship class which responds to user input
for movement and shooting.
"""
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, Sequence

import pygame

from logic.Bullet import Bullet
from logic.GameObject import GameObject
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE,
    SPACESHIP_ACCELERATION, SPACESHIP_FRICTION,
    SPACESHIP_ROTATION_SPEED, SPACESHIP_RADIUS,
    RESPAWN_DELAY, HYPERSPACE_COOLDOWN
)

if TYPE_CHECKING:
    from logic.Asteroid import Asteroid


class Spaceship(GameObject):
    """
    Spaceship class representing the player-controlled ship.

    Inherits from GameObject and implements its abstract methods.
    The spaceship responds to keyboard input for movement and shooting,
    and can collide with asteroids resulting in loss of life.
    
    Includes original Asteroids features:
    - Hyperspace: Teleport to random location (risky!)
    - Invulnerability after respawn
    
    Attributes:
        x: Horizontal position of the spaceship
        y: Vertical position of the spaceship
        angle: Current rotation angle in degrees
        velocity_x: Horizontal velocity component
        velocity_y: Vertical velocity component
        acceleration: Rate of speed increase when thrusting
        friction: Slowdown coefficient applied each frame
        radius: Collision detection radius
        alive: Whether the spaceship is still active
        invulnerable: Whether spaceship is temporarily invulnerable
        invulnerable_until: Timestamp when invulnerability ends
        hyperspace_available: Timestamp when hyperspace can be used again
    """

    def __init__(self) -> None:
        """
        Initialize a new spaceship at the center of the screen.

        Sets up the spaceship's position, movement properties, and collision radius.
        """
        self.x: float = SCREEN_WIDTH / 2
        self.y: float = SCREEN_HEIGHT / 2
        self.angle: float = -90  # Facing up (negative Y is up in pygame)
        self.velocity_x: float = 0
        self.velocity_y: float = 0
        self.acceleration: float = SPACESHIP_ACCELERATION
        self.friction: float = SPACESHIP_FRICTION
        self.radius: int = SPACESHIP_RADIUS
        self.alive: bool = True
        
        # Invulnerability (after respawn)
        self.invulnerable: bool = False
        self.invulnerable_until: int = 0
        
        # Hyperspace cooldown
        self.hyperspace_available: int = 0
        
        # Visual blinking for invulnerability
        self._blink_timer: int = 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the spaceship on the screen as a triangle pointing in its direction.
        Blinks when invulnerable.

        Args:
            screen: Pygame surface to draw on

        Implements the abstract draw method from GameObject.
        """
        # Blink effect when invulnerable
        if self.invulnerable:
            self._blink_timer += 1
            if self._blink_timer % 10 < 5:  # Blink every 5 frames
                return  # Don't draw this frame
        
        # Calculate triangle points for spaceship shape
        front_point = (
            self.x + math.cos(math.radians(self.angle)) * self.radius,
            self.y + math.sin(math.radians(self.angle)) * self.radius
        )
        left_point = (
            self.x + math.cos(math.radians(self.angle + 140)) * (self.radius * 0.67),
            self.y + math.sin(math.radians(self.angle + 140)) * (self.radius * 0.67)
        )
        right_point = (
            self.x + math.cos(math.radians(self.angle - 140)) * (self.radius * 0.67),
            self.y + math.sin(math.radians(self.angle - 140)) * (self.radius * 0.67)
        )

        pygame.draw.polygon(screen, WHITE, [front_point, left_point, right_point], 2)

    def update(self, keys: Sequence[bool], delta_time: float = 1.0) -> None:
        """
        Update the spaceship's state based on keyboard input.

        Handles rotation, acceleration, and movement with screen wrapping.

        Args:
            keys: Pygame key state sequence from pygame.key.get_pressed()
            delta_time: Time multiplier for frame-independent movement

        Implements the abstract update method from GameObject.
        """
        # Check invulnerability timer
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time >= self.invulnerable_until:
                self.invulnerable = False
                self._blink_timer = 0
        
        if keys[pygame.K_LEFT]:
            self.angle -= SPACESHIP_ROTATION_SPEED * delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += SPACESHIP_ROTATION_SPEED * delta_time
        if keys[pygame.K_UP]:
            self.velocity_x += math.cos(math.radians(self.angle)) * self.acceleration * delta_time
            self.velocity_y += math.sin(math.radians(self.angle)) * self.acceleration * delta_time

        # Apply friction to gradually slow down
        friction_factor = self.friction ** delta_time
        self.velocity_x *= friction_factor
        self.velocity_y *= friction_factor

        # Update position with screen wrapping
        self.x = (self.x + self.velocity_x * delta_time) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y * delta_time) % SCREEN_HEIGHT

    def shoot(self) -> Bullet:
        """
        Create a new bullet fired from the spaceship's position.

        The bullet travels in the direction the spaceship is facing.

        Returns:
            A new bullet instance
        """
        angle_radians = math.radians(self.angle)
        bullet_direction_x = math.cos(angle_radians)
        bullet_direction_y = math.sin(angle_radians)
        return Bullet(self.x, self.y, bullet_direction_x, bullet_direction_y)

    def hyperspace(self) -> bool:
        """
        Teleport to a random location on the screen.
        
        This is a risky move from the original Asteroids - you might
        teleport right into an asteroid!
        
        Returns:
            True if hyperspace was activated, False if on cooldown
        """
        current_time = pygame.time.get_ticks()
        if current_time < self.hyperspace_available:
            return False
        
        # Teleport to random location
        self.x = random.uniform(50, SCREEN_WIDTH - 50)
        self.y = random.uniform(50, SCREEN_HEIGHT - 50)
        
        # Stop all momentum
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Set cooldown
        self.hyperspace_available = current_time + HYPERSPACE_COOLDOWN
        
        return True

    def respawn(self) -> None:
        """
        Respawn the spaceship at the center of the screen.
        
        Grants temporary invulnerability.
        """
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.angle = -90  # Facing up
        self.velocity_x = 0
        self.velocity_y = 0
        self.alive = True
        
        # Grant invulnerability
        self.invulnerable = True
        self.invulnerable_until = pygame.time.get_ticks() + RESPAWN_DELAY
        self._blink_timer = 0

    def collides_with(self, asteroid: Asteroid) -> bool:
        """
        Check if the spaceship collides with an asteroid.

        Uses circular collision detection based on the distance between objects.
        Returns False if spaceship is invulnerable.

        Args:
            asteroid: The asteroid to check collision with

        Returns:
            True if colliding (and not invulnerable), False otherwise
        """
        if self.invulnerable:
            return False
            
        distance = math.hypot(self.x - asteroid.x, self.y - asteroid.y)
        return distance < self.radius + asteroid.get_radius()
    
    def collides_with_ufo(self, ufo) -> bool:
        """
        Check if the spaceship collides with a UFO.

        Args:
            ufo: The UFO to check collision with

        Returns:
            True if colliding (and not invulnerable), False otherwise
        """
        if self.invulnerable:
            return False
            
        distance = math.hypot(self.x - ufo.x, self.y - ufo.y)
        return distance < self.radius + ufo.get_radius()
    
    def hit_by_bullet(self, bullet: Bullet) -> bool:
        """
        Check if the spaceship is hit by a bullet.

        Args:
            bullet: The bullet to check

        Returns:
            True if hit (and not invulnerable), False otherwise
        """
        if self.invulnerable:
            return False
            
        distance = math.hypot(self.x - bullet.x, self.y - bullet.y)
        return distance < self.radius + bullet.radius