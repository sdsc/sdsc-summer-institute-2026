import numpy as np
import pytest

from skydiver.physics import (
    terminal_velocity,
    time_to_fraction,
    velocity_at_time,
)


def test_earth_terminal_velocity():
    result = terminal_velocity(mass_kg=80, drag_coefficient=0.26)
    assert result == pytest.approx(54.95, rel=0.01)


def test_velocity_approaches_negative_terminal_velocity():
    limit = terminal_velocity(mass_kg=80, drag_coefficient=0.26)
    result = velocity_at_time(
        time_s=np.array([0.0, 100.0]),
        mass_kg=80,
        drag_coefficient=0.26,
    )
    assert result[0] == pytest.approx(0.0)
    assert result[-1] == pytest.approx(-limit, rel=1e-6)


def test_time_to_99_percent():
    seconds = time_to_fraction(0.99, mass_kg=80, drag_coefficient=0.26)
    assert seconds == pytest.approx(14.83, rel=0.01)


@pytest.mark.parametrize(
    ("mass", "drag", "gravity"),
    [(0, 0.26, 9.81), (80, 0, 9.81), (80, 0.26, -9.81)],
)
def test_invalid_parameters_fail_clearly(mass, drag, gravity):
    with pytest.raises(ValueError):
        terminal_velocity(mass, drag, gravity)
