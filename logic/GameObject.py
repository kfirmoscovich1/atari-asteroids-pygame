"""
Abstract base class module defining the interface for all game objects.
This module provides the GameObject abstract class that ensures all game objects
implement the necessary methods for updating and rendering.
"""
from abc import ABC, abstractmethod
from typing import Any

import pygame


class GameObject(ABC):
    """
    Abstract base class that defines the interface for all game objects.

    This class serves as a contract that ensures all game objects implement
    the required functionality for updating their state and rendering themselves.
    Using this abstract base class enables polymorphism in the game architecture,
    allowing different types of objects to be handled uniformly.

    Attributes:
        x: Horizontal position of the game object
        y: Vertical position of the game object
    """

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        """
        Update the game object's state for the next frame.
        
        This includes position, movement, or any other time-based changes.
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the game object on the screen.
        
        Args:
            screen: The pygame surface to draw on
        """
        pass