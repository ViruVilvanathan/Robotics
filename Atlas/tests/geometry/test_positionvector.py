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

def test_displacement():
    start = Position(1, 2)
    end = Position(4, 6)

    displacement = start.vector_to(end)

    assert displacement.x == 3
    assert displacement.y == 4

def test_displacement_negative():
    start = Position(4, 6)
    end = Position(1, 2)

    displacement = start.vector_to(end)

    assert displacement.x == -3
    assert displacement.y == -4

def test_displacement_zero():
    start = Position(2, 3)
    end = Position(2, 3)

    displacement = start.vector_to(end)

    assert displacement.x == 0
    assert displacement.y == 0

def test_distance():
    start = Position(1, 2)
    end = Position(4, 6)

    distance = start.distance_to(end)

    assert distance == 5.0

def test_distance_zero():
    start = Position(2, 3)
    end = Position(2, 3)

    distance = start.distance_to(end)

    assert distance == 0.0

def test_distance_negative():
    start = Position(4, 6)
    end = Position(1, 2)

    distance = start.distance_to(end)

    assert distance == 5.0

def test_distance_with_floats_symmetry():
    start = Position(1.5, 2.5)
    end = Position(4.5, 6.5)

    distance = start.distance_to(end)

    assert distance == pytest.approx(end.distance_to(start))
