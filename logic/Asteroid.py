"""
Asteroid class implementation for the Asteroids game.
This module contains the Asteroid class which represents destructible space rocks
that the player must avoid and shoot.
"""
from __future__ import annotations

import math
import random
from typing import List, Tuple

import pygame

from logic.GameObject import GameObject
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MIN_VERTICES, MAX_VERTICES,
    MIN_RADIUS_FACTOR, MAX_RADIUS_FACTOR,
    ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED,
    ASTEROID_SCORE,
    YELLOW, PINK, ORANGE, PURPLE
)

# Type alias for RGB color tuples
Color = Tuple[int, int, int]
Point = Tuple[float, float]


class Asteroid(GameObject):
    """
    Asteroid class representing the destructible space rocks in the game.

    Inherits from GameObject and implements its abstract methods.
    Asteroids have random polygonal shapes, colors, and movement patterns.
    They can be destroyed by the player's bullets and split into smaller pieces.
    
    Attributes:
        x: Horizontal position of the asteroid
        y: Vertical position of the asteroid
        size: Size category (1=small, 2=medium, 3=large)
        velocity_x: Horizontal velocity component
        velocity_y: Vertical velocity component
        shape: List of points defining the asteroid's polygon
        color: RGB color tuple for rendering
    """

    # Available asteroid colors
    COLORS: List[Color] = [YELLOW, PINK, ORANGE, PURPLE]

    def __init__(self, x: float, y: float, size: int) -> None:
        """
        Initialize a new asteroid object.

        Args:
            x: Initial x-coordinate position
            y: Initial y-coordinate position
            size: Size category of the asteroid (1=small, 2=medium, 3=large)
        """
        self.x: float = x
        self.y: float = y
        self.size: int = size

        # Generate random velocity with finer control (divide by 10 for float precision)
        self.velocity_x: float = random.randint(
            ASTEROID_MIN_SPEED * 10, ASTEROID_MAX_SPEED * 10
        ) / 10
        self.velocity_y: float = random.randint(
            ASTEROID_MIN_SPEED * 10, ASTEROID_MAX_SPEED * 10
        ) / 10

        self.shape: List[Point] = self._generate_shape()
        self.color: Color = self._pick_color()

    def _generate_shape(self) -> List[Point]:
        """
        Generate a random polygonal shape for the asteroid.

        Creates a polygon with random number of vertices and variable radius
        to give asteroids an irregular appearance.

        Returns:
            List of coordinate tuples representing the asteroid's shape
        """
        points: List[Point] = []
        num_vertices = random.randint(MIN_VERTICES, MAX_VERTICES)
        angle_step = 360 / num_vertices
        
        for i in range(num_vertices):
            angle = math.radians(i * angle_step)
            radius = self.size * random.randint(MIN_RADIUS_FACTOR, MAX_RADIUS_FACTOR)
            points.append((math.cos(angle) * radius, math.sin(angle) * radius))
            
        return points

    def _pick_color(self) -> Color:
        """
        Randomly select a color for the asteroid.

        Returns:
            RGB color values as a tuple
        """
        return random.choice(self.COLORS)

    def update(self, delta_time: float = 1.0) -> None:
        """
        Update the asteroid's position based on its velocity.

        Handles screen wrapping when asteroid moves off-screen.
        Implements the abstract update method from GameObject.
        
        Args:
            delta_time: Time multiplier for frame-independent movement
        """
        self.x = (self.x + self.velocity_x * delta_time) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y * delta_time) % SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the asteroid on the screen.

        Args:
            screen: Pygame surface to draw on

        Implements the abstract draw method from GameObject.
        """
        transformed_points = [(self.x + x, self.y + y) for x, y in self.shape]
        pygame.draw.polygon(screen, self.color, transformed_points)

    def get_radius(self) -> float:
        """
        Get the effective collision radius of the asteroid.

        Returns:
            Radius for collision detection purposes
        """
        return float(self.size * 10)

    def get_score(self) -> int:
        """
        Get the score value for destroying this asteroid.

        Returns:
            Point value based on asteroid size (smaller = higher value)
        """
        return ASTEROID_SCORE.get(self.size, 0)

    def split(self) -> List[Asteroid]:
        """
        Split the asteroid into smaller pieces when hit.

        Returns:
            List of two smaller asteroids, or empty list if already at minimum size
        """
        if self.size > 1:
            return [
                Asteroid(self.x, self.y, self.size - 1),
                Asteroid(self.x, self.y, self.size - 1)
            ]
        return []

    @staticmethod
    def random_spawn() -> Asteroid:
        """
        Create a new asteroid at a random position outside the visible screen.

        This static method is used to spawn new asteroids during gameplay.
        Asteroids spawn just outside the screen edges to create a natural
        entry into the game area.

        Returns:
            A new asteroid instance with random size and position
        """
        spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if spawn_side == 'top':
            x, y = random.randint(0, SCREEN_WIDTH), -10
        elif spawn_side == 'bottom':
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10
        elif spawn_side == 'left':
            x, y = -10, random.randint(0, SCREEN_HEIGHT)
        else:  # right
            x, y = SCREEN_WIDTH + 10, random.randint(0, SCREEN_HEIGHT)
            
        return Asteroid(x, y, random.choice([1, 2, 3]))