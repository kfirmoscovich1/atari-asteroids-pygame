"""
Bullet class implementation for the Asteroids game.
This module contains the Bullet class which represents projectiles fired by the spaceship
that can destroy asteroids.
"""
import pygame

from logic.GameObject import GameObject
from utils.Constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BULLET_SPEED


class Bullet(GameObject):
    """
    Bullet class representing projectiles fired by the player's spaceship.

    Inherits from GameObject and implements its abstract methods.
    Bullets travel in a straight line based on the direction they were fired.
    They destroy asteroids on contact and disappear when they leave the screen.
    
    Attributes:
        x: Current x-coordinate position
        y: Current y-coordinate position
        direction_x: X-component of velocity
        direction_y: Y-component of velocity
        radius: Collision radius of the bullet
    """

    def __init__(self, x: float, y: float, direction_x: float, direction_y: float) -> None:
        """
        Initialize a new bullet object.

        Args:
            x: Initial x-coordinate position (typically the spaceship's position)
            y: Initial y-coordinate position (typically the spaceship's position)
            direction_x: X-component of direction vector (-1 to 1)
            direction_y: Y-component of direction vector (-1 to 1)
        """
        self.x: float = x
        self.y: float = y
        # Multiply by BULLET_SPEED constant for consistent speed
        self.direction_x: float = direction_x * BULLET_SPEED
        self.direction_y: float = direction_y * BULLET_SPEED
        self.radius: int = 3
        
        # Create a transparent surface for the bullet
        self.image: pygame.Surface = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )
        # Draw the bullet as a white circle
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)
        # Create a rectangle for collision detection and drawing
        self.rect: pygame.Rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, delta_time: float = 1.0) -> None:
        """
        Update the bullet's position based on its direction.

        Moves the bullet along its trajectory each frame.
        Implements the abstract update method from GameObject.
        
        Args:
            delta_time: Time multiplier for frame-independent movement
        """
        self.x += self.direction_x * delta_time
        self.y += self.direction_y * delta_time
        # Update the rect position to match the bullet's position
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the bullet on the screen.

        Args:
            screen: Pygame surface to draw on

        Implements the abstract draw method from GameObject.
        """
        screen.blit(self.image, self.rect)

    def is_on_screen(self) -> bool:
        """
        Check if the bullet is still within the screen boundaries.

        Returns:
            True if the bullet is on screen, False if it has left the screen
            and should be removed
        """
        return 0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT