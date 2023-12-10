import pytest
from settings import Settings
import math

# Test IDs for parametrization
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Parametrized test for happy path scenarios
@pytest.mark.parametrize("ship_speed, bullet_speed, alien_speed, alien_points, speedup_scale, score_scale, expected", [
    (1.0, 1.0, 1.0, 50, 2.0, 2.0, (2.0, 2.0, 2.0, 100)),  # Doubling speeds and points
    (0.5, 0.5, 0.5, 20, 3.0, 1.5, (1.5, 1.5, 1.5, 30)),   # Tripling speeds, 1.5x points
    (3.0, 4.0, 2.0, 10, 1.1, 1.2, (3.3, 4.4, 2.2, 12)),   # 10% increase in speeds, 20% in points
], ids=[HAPPY_PATH_ID + "_1", HAPPY_PATH_ID + "_2", HAPPY_PATH_ID + "_3"])
def test_increase_speed_happy_path(ship_speed, bullet_speed, alien_speed, alien_points, speedup_scale, score_scale, expected):
    # Arrange
    settings = Settings()
    settings.ship_speed = ship_speed
    settings.bullet_speed = bullet_speed
    settings.alien_speed = alien_speed
    settings.alien_points = alien_points
    settings.speedup_scale = speedup_scale
    settings.score_scale = score_scale

    # Act
    settings.increase_speed()

    # Assert
    assert math.isclose(settings.ship_speed, expected[0], rel_tol=1e-9)
    assert settings.bullet_speed == expected[1]
    assert settings.alien_speed == expected[2]
    assert settings.alien_points == expected[3]

# Parametrized test for edge cases
@pytest.mark.parametrize("ship_speed, bullet_speed, alien_speed, alien_points, speedup_scale, score_scale, expected", [
    (0.0, 0.0, 0.0, 0, 2.0, 2.0, (0.0, 0.0, 0.0, 0)),  # Zero speeds and points
    (-1.0, -1.0, -1.0, 50, 2.0, 2.0, (-2.0, -2.0, -2.0, 100)),  # Negative speeds, doubling points
], ids=[EDGE_CASE_ID + "_1", EDGE_CASE_ID + "_2"])
def test_increase_speed_edge_cases(ship_speed, bullet_speed, alien_speed, alien_points, speedup_scale, score_scale, expected):
    # Arrange
    settings = Settings()
    settings.ship_speed = ship_speed
    settings.bullet_speed = bullet_speed
    settings.alien_speed = alien_speed
    settings.alien_points = alien_points
    settings.speedup_scale = speedup_scale
    settings.score_scale = score_scale

    # Act
    settings.increase_speed()

    # Assert
    assert settings.ship_speed == expected[0]
    assert settings.bullet_speed == expected[1]
    assert settings.alien_speed == expected[2]
    assert settings.alien_points == expected[3]

# Parametrized test for error cases
@pytest.mark.parametrize("ship_speed, bullet_speed, alien_speed, alien_points, speedup_scale, score_scale", [
    ("fast", 1.0, 1.0, 50, 2.0, 2.0),  # Non-numeric speed
    (1.0, "fast", 1.0, 50, 2.0, 2.0),  # Non-numeric speed
    (1.0, 1.0, "fast", 50, 2.0, 2.0),  # Non-numeric speed
    (1.0, 1.0, 1.0, "fifty", 2.0, 2.0),  # Non-numeric points
], ids=[ERROR_CASE_ID + "_1", ERROR_CASE_ID + "_2", ERROR_CASE_ID + "_3", ERROR_CASE_ID + "_4"])
def test_increase_speed_error_cases(ship_speed, bullet_speed, alien_speed, alien_points, speedup_scale, score_scale):
    # Arrange
    settings = Settings()
    settings.ship_speed = ship_speed
    settings.bullet_speed = bullet_speed
    settings.alien_speed = alien_speed
    settings.alien_points = alien_points
    settings.speedup_scale = speedup_scale
    settings.score_scale = score_scale

    # Act / Assert
    with pytest.raises(TypeError):
        settings.increase_speed()
