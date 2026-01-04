"""
UI package for the Asteroids game.
Contains user interface screens including the main menu, instructions,
and end game screen.

Note: Use direct imports from submodules to avoid circular import issues:
    from ui.Menu import Menu
    from ui.EndScreen import EndScreen
"""

# Export names for package documentation
__all__ = [
    "Menu",
    "Instructions",
    "EndScreen",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "Menu":
        from ui.Menu import Menu
        return Menu
    elif name == "Instructions":
        from ui.Instructions import Instructions
        return Instructions
    elif name == "EndScreen":
        from ui.EndScreen import EndScreen
        return EndScreen
    raise AttributeError(f"module 'ui' has no attribute '{name}'")
