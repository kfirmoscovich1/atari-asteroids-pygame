"""
Collision detection module for the Asteroids game.
This module contains utility functions for detecting collisions between game objects
using circle-based collision detection.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.Asteroid import Asteroid
    from logic.Bullet import Bullet


def check_collision(asteroid: Asteroid, bullet: Bullet) -> bool:
    """
    Determine if an asteroid and bullet are colliding.
    
    Uses circle collision detection by comparing the distance between
    objects to the sum of their radii. This is an efficient O(1) collision
    check suitable for the game's needs.

    Args:
        asteroid: The asteroid object to check
        bullet: The bullet object to check

    Returns:
        True if objects are colliding, False otherwise
    """
    # Calculate distance using the Pythagorean theorem
    dx = asteroid.x - bullet.x
    dy = asteroid.y - bullet.y
    distance = math.sqrt(dx * dx + dy * dy)

    # Check if distance is less than combined radii
    return distance < asteroid.get_radius() + bullet.radius


def check_circle_collision(
    x1: float, y1: float, r1: float,
    x2: float, y2: float, r2: float
) -> bool:
    """
    Generic circle-based collision detection.
    
    This function can be used for any two circular objects in the game.

    Args:
        x1: X position of first circle
        y1: Y position of first circle
        r1: Radius of first circle
        x2: X position of second circle
        y2: Y position of second circle
        r2: Radius of second circle

    Returns:
        True if circles are overlapping, False otherwise
    """
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance < r1 + r2