"""
Unit tests for collision detection functions.
These tests verify that the collision detection logic works correctly
without requiring pygame initialization.
"""
import math
import pytest

# Import the pure math collision function
from logic.Collision import check_circle_collision


class TestCircleCollision:
    """Tests for circle-based collision detection."""

    def test_overlapping_circles_collide(self):
        """Two overlapping circles should be detected as colliding."""
        # Circle 1 at (0, 0) with radius 10
        # Circle 2 at (5, 0) with radius 10
        # Distance = 5, combined radii = 20, so they overlap
        assert check_circle_collision(0, 0, 10, 5, 0, 10) is True

    def test_touching_circles_collide(self):
        """Two circles that are just touching should be detected as colliding."""
        # Circle 1 at (0, 0) with radius 10
        # Circle 2 at (19, 0) with radius 10
        # Distance = 19, combined radii = 20, so they touch
        assert check_circle_collision(0, 0, 10, 19, 0, 10) is True

    def test_separate_circles_no_collision(self):
        """Two circles that are not touching should not collide."""
        # Circle 1 at (0, 0) with radius 10
        # Circle 2 at (100, 0) with radius 10
        # Distance = 100, combined radii = 20, so they don't collide
        assert check_circle_collision(0, 0, 10, 100, 0, 10) is False

    def test_circles_just_apart(self):
        """Two circles that are just barely apart should not collide."""
        # Circle 1 at (0, 0) with radius 10
        # Circle 2 at (21, 0) with radius 10
        # Distance = 21, combined radii = 20, so they don't collide
        assert check_circle_collision(0, 0, 10, 21, 0, 10) is False

    def test_same_position_circles_collide(self):
        """Two circles at the same position should definitely collide."""
        assert check_circle_collision(50, 50, 10, 50, 50, 10) is True

    def test_diagonal_collision(self):
        """Test collision detection along diagonal."""
        # Circle 1 at (0, 0) with radius 10
        # Circle 2 at (10, 10) with radius 10
        # Distance = sqrt(200) ≈ 14.14, combined radii = 20
        assert check_circle_collision(0, 0, 10, 10, 10, 10) is True

    def test_diagonal_no_collision(self):
        """Test non-collision along diagonal."""
        # Circle 1 at (0, 0) with radius 5
        # Circle 2 at (20, 20) with radius 5
        # Distance = sqrt(800) ≈ 28.28, combined radii = 10
        assert check_circle_collision(0, 0, 5, 20, 20, 5) is False

    def test_negative_coordinates(self):
        """Test collision detection with negative coordinates."""
        # Circle 1 at (-10, -10) with radius 5
        # Circle 2 at (-5, -10) with radius 5
        # Distance = 5, combined radii = 10
        assert check_circle_collision(-10, -10, 5, -5, -10, 5) is True

    def test_float_precision(self):
        """Test collision detection with floating point coordinates."""
        # Circles that are very close
        assert check_circle_collision(0.0, 0.0, 10.0, 19.9999, 0.0, 10.0) is True

    def test_zero_radius(self):
        """Test collision detection with zero radius (point)."""
        # Point at (5, 5) inside circle at (0, 0) with radius 10
        assert check_circle_collision(0, 0, 10, 5, 5, 0) is True
        
        # Point at (20, 0) outside circle at (0, 0) with radius 10
        assert check_circle_collision(0, 0, 10, 20, 0, 0) is False


class TestCollisionMath:
    """Tests for the mathematical accuracy of collision detection."""

    def test_distance_calculation_accuracy(self):
        """Verify that distance calculations are accurate."""
        # Known Pythagorean triple: 3-4-5
        # Circle 1 at (0, 0) with radius 2
        # Circle 2 at (3, 4) with radius 2
        # Distance = 5, combined radii = 4
        assert check_circle_collision(0, 0, 2, 3, 4, 2) is False
        
        # With larger radii that would cause collision
        assert check_circle_collision(0, 0, 3, 3, 4, 3) is True

    def test_symmetry(self):
        """Collision detection should be symmetric."""
        # Order of circles shouldn't matter
        result1 = check_circle_collision(0, 0, 10, 15, 0, 10)
        result2 = check_circle_collision(15, 0, 10, 0, 0, 10)
        assert result1 == result2
