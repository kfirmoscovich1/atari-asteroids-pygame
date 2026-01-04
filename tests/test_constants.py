"""
Unit tests for game constants and configuration.
These tests verify that constants are properly defined and have valid values.
"""
import pytest
from utils.Constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SPACESHIP_ACCELERATION, SPACESHIP_FRICTION,
    SPACESHIP_ROTATION_SPEED, SPACESHIP_RADIUS,
    ASTEROID_SCORE, ASTEROID_SIZES,
    MIN_VERTICES, MAX_VERTICES,
    WHITE, BLACK,
)


class TestScreenConstants:
    """Tests for screen dimension constants."""

    def test_screen_width_is_positive(self):
        """Screen width must be a positive integer."""
        assert isinstance(SCREEN_WIDTH, int)
        assert SCREEN_WIDTH > 0

    def test_screen_height_is_positive(self):
        """Screen height must be a positive integer."""
        assert isinstance(SCREEN_HEIGHT, int)
        assert SCREEN_HEIGHT > 0

    def test_reasonable_screen_size(self):
        """Screen should be a reasonable size for gameplay."""
        assert 400 <= SCREEN_WIDTH <= 1920
        assert 300 <= SCREEN_HEIGHT <= 1080


class TestGameplayConstants:
    """Tests for gameplay-related constants."""

    def test_fps_is_reasonable(self):
        """FPS should be a reasonable value for smooth gameplay."""
        assert isinstance(FPS, int)
        assert 30 <= FPS <= 144

    def test_spaceship_physics_valid(self):
        """Spaceship physics constants should be valid."""
        assert SPACESHIP_ACCELERATION > 0
        assert 0 < SPACESHIP_FRICTION <= 1
        assert SPACESHIP_ROTATION_SPEED > 0
        assert SPACESHIP_RADIUS > 0


class TestAsteroidConstants:
    """Tests for asteroid-related constants."""

    def test_asteroid_sizes_valid(self):
        """Asteroid sizes list should be valid."""
        assert len(ASTEROID_SIZES) > 0
        assert all(isinstance(size, int) for size in ASTEROID_SIZES)
        assert all(size > 0 for size in ASTEROID_SIZES)

    def test_asteroid_scores_defined(self):
        """All asteroid sizes should have corresponding scores."""
        for size in ASTEROID_SIZES:
            assert size in ASTEROID_SCORE
            assert ASTEROID_SCORE[size] > 0

    def test_smaller_asteroids_worth_more(self):
        """Smaller asteroids should be worth more points."""
        sizes = sorted(ASTEROID_SIZES)
        scores = [ASTEROID_SCORE[size] for size in sizes]
        # Verify scores decrease as size increases
        assert scores == sorted(scores, reverse=True)

    def test_vertex_counts_valid(self):
        """Vertex counts should be valid for polygon generation."""
        assert MIN_VERTICES >= 3  # Minimum for a polygon
        assert MAX_VERTICES >= MIN_VERTICES


class TestColorConstants:
    """Tests for color constants."""

    def test_colors_are_rgb_tuples(self):
        """Colors should be valid RGB tuples."""
        for color in [WHITE, BLACK]:
            assert isinstance(color, tuple)
            assert len(color) == 3
            assert all(isinstance(c, int) for c in color)
            assert all(0 <= c <= 255 for c in color)

    def test_white_is_white(self):
        """White should be (255, 255, 255)."""
        assert WHITE == (255, 255, 255)

    def test_black_is_black(self):
        """Black should be (0, 0, 0)."""
        assert BLACK == (0, 0, 0)
