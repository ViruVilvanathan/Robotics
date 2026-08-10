from atlas.geometry.positionvector import Position, Vector
import pytest


def test_position_creation():
    position = Position(2, 3)

    assert position.x == 2
    assert position.y == 3


def test_position_accepts_floats():
    position = Position(1.5, -2.7)

    assert position.x == 1.5
    assert position.y == -2.7


def test_position_repr():
    position = Position(2, 3)

    assert repr(position) == "Position(x=2, y=3)"


def test_vector_creation():
    vector = Vector(3, 4)

    assert vector.x == 3
    assert vector.y == 4


def test_vector_accepts_negative_values():
    vector = Vector(-3, 4)

    assert vector.x == -3
    assert vector.y == 4


def test_vector_repr():
    vector = Vector(3, 4)

    assert repr(vector) == "Vector(x=3, y=4)"

def test_vector_magnitude():
    vector = Vector(3, 4)

    assert vector.magnitude() == 5.0


def test_zero_vector_magnitude():
    vector = Vector(0, 0)

    assert vector.magnitude() == 0.0


def test_negative_vector_magnitude():
    vector = Vector(-3, -4)

    assert vector.magnitude() == 5.0

def test_vector_normalization():
    vector = Vector(3, 4)

    normalized = vector.normalized()

    assert normalized.x == pytest.approx(0.6)
    assert normalized.y == pytest.approx(0.8)
    assert normalized.magnitude() == pytest.approx(1.0)


def test_zero_vector_cannot_be_normalized():
    vector = Vector(0, 0)

    with pytest.raises(ValueError):
        vector.normalized()