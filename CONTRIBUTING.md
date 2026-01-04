# Contributing to Asteroids

First off, thank you for considering contributing to this project! 🎮

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title** describing the bug
2. **Steps to reproduce** the issue
3. **Expected behavior** vs **actual behavior**
4. **Screenshots** if applicable
5. **Environment info** (OS, Python version, Pygame version)

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:

1. **Clear description** of the feature
2. **Use case** - why would this be useful?
3. **Possible implementation** ideas (optional)

### Pull Requests

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the code style guidelines below
4. **Test your changes** to ensure nothing is broken
5. **Commit** with a clear message: `git commit -m 'Add amazing feature'`
6. **Push** to your fork: `git push origin feature/amazing-feature`
7. **Open a Pull Request** with a clear description

## Code Style Guidelines

### Python

- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example

```python
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate the Euclidean distance between two points.
    
    Args:
        x1: X coordinate of first point
        y1: Y coordinate of first point
        x2: X coordinate of second point
        y2: Y coordinate of second point
    
    Returns:
        The distance between the two points
    """
    return math.hypot(x2 - x1, y2 - y1)
```

### Commits

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep commits focused on a single change

### File Organization

- **logic/** - Game mechanics and entities
- **ui/** - User interface screens
- **utils/** - Helper functions and constants
- **tests/** - Unit tests
- **assets/** - Images, sounds, fonts

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/kfirmoscovich1/atari-asteroids-pygame.git
cd atari-asteroids-pygame
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # if available
   ```

4. Run the game to verify setup:
   ```bash
   python Program.py
   ```

## Testing

- Add tests for new functionality
- Run existing tests before submitting: `python -m pytest tests/`
- Ensure all tests pass

## Questions?

Feel free to open an issue for any questions about contributing!

---

Thank you for helping make this project better! 🚀
