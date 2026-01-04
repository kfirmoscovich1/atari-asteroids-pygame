"""
Logic package for the Asteroids game.
Contains core game logic components including entities, collision detection,
and the main game loop.

Note: Use direct imports from submodules to avoid circular import issues:
    from logic.Collision import check_collision
    from logic.Spaceship import Spaceship
"""

# Export names for package documentation
__all__ = [
    "run_game",
    "GameObject",
    "Spaceship",
    "Asteroid",
    "Bullet",
    "UFO",
    "check_collision",
    "check_circle_collision",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "run_game":
        from logic.Game import run_game
        return run_game
    elif name == "GameObject":
        from logic.GameObject import GameObject
        return GameObject
    elif name == "Spaceship":
        from logic.Spaceship import Spaceship
        return Spaceship
    elif name == "Asteroid":
        from logic.Asteroid import Asteroid
        return Asteroid
    elif name == "Bullet":
        from logic.Bullet import Bullet
        return Bullet
    elif name == "UFO":
        from logic.UFO import UFO
        return UFO
    elif name == "check_collision":
        from logic.Collision import check_collision
        return check_collision
    elif name == "check_circle_collision":
        from logic.Collision import check_circle_collision
        return check_circle_collision
    raise AttributeError(f"module 'logic' has no attribute '{name}'")
