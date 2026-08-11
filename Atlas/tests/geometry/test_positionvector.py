from numpy import sqrt

from atlas.geometry.positionvector import Position, Vector
import pytest


def test_position_creation():
    position = Position(2, 3, 4)

    assert position.x == 2
    assert position.y == 3


def test_position_accepts_floats():
    position = Position(1.5, -2.7, 0)

    assert position.x == 1.5
    assert position.y == -2.7
    assert position.z == 0

def test_position_repr():
    position = Position(2, 3, 4)

    assert repr(position) == "Position(x=2, y=3, z=4)"


def test_vector_creation():
    vector = Vector(3, 4, 5)

    assert vector.x == 3
    assert vector.y == 4
    assert vector.z == 5


def test_vector_accepts_negative_values():
    vector = Vector(-3, 4, -5)

    assert vector.x == -3
    assert vector.y == 4
    assert vector.z == -5


def test_vector_repr():
    vector = Vector(3, 4, 5)

    assert repr(vector) == "Vector(x=3, y=4, z=5)"

def test_vector_magnitude():
    vector = Vector(3, 4, 5)

    assert vector.magnitude() == pytest.approx(sqrt(3**2 + 4**2 + 5**2))


def test_zero_vector_magnitude():
    vector = Vector(0, 0, 0)

    assert vector.magnitude() == 0.0


def test_negative_vector_magnitude():
    vector = Vector(-3, -4, -5)

    assert vector.magnitude() == pytest.approx(sqrt((-3)**2 + (-4)**2 + (-5)**2))

def test_vector_normalization():
    vector = Vector(3, 4, 5)

    normalized = vector.normalized()

    assert normalized.magnitude() == pytest.approx(1.0)
    assert normalized.x == pytest.approx(3 / vector.magnitude())
    assert normalized.y == pytest.approx(4 / vector.magnitude())
    assert normalized.z == pytest.approx(5 / vector.magnitude())


def test_zero_vector_cannot_be_normalized():
    vector = Vector(0, 0, 0)

    with pytest.raises(ValueError):
        vector.normalized()

def test_displacement():
    start = Position(1, 2, 3)
    end = Position(4, 6, 7)

    displacement = start.vector_to(end)

    assert displacement.x == 3
    assert displacement.y == 4
    assert displacement.z == 4

def test_displacement_negative():
    start = Position(4, 6, 7)
    end = Position(1, 2, 3)

    displacement = start.vector_to(end)

    assert displacement.x == -3
    assert displacement.y == -4
    assert displacement.z == -4

def test_displacement_zero():
    start = Position(2, 3, 4)
    end = Position(2, 3, 4)

    displacement = start.vector_to(end)

    assert displacement.x == 0
    assert displacement.y == 0
    assert displacement.z == 0

def test_distance():
    start = Position(1, 2, 3)
    end = Position(4, 6, 7)

    distance = start.distance_to(end)

    assert distance == pytest.approx(sqrt((4-1)**2 + (6-2)**2 + (7-3)**2))

def test_distance_zero():
    start = Position(2, 3, 4)
    end = Position(2, 3, 4)

    distance = start.distance_to(end)

    assert distance == 0.0

def test_distance_negative():
    start = Position(4, 6, 7)
    end = Position(1, 2, 3)

    distance = start.distance_to(end)

    assert distance == pytest.approx(sqrt((1-4)**2 + (2-6)**2 + (3-7)**2))

def test_distance_with_floats_symmetry():
    start = Position(1.5, 2.5, 3.5)
    end = Position(4.5, 6.5, 7.5)

    distance = start.distance_to(end)

    assert distance == pytest.approx(end.distance_to(start))

Vectordata = [
    [Vector(3, 4, 5), Vector(-4, 3, 5), 25],
    [Vector(3, 4, -5), Vector(3, 4, 5), 0],
    [Vector(3, 4, 5), Vector(0, 0, 0), 0],
]

@pytest.mark.parametrize("vector1, vector2, expected", Vectordata)

def test_dot_product(vector1, vector2, expected):

    dot_product = vector1.dot(vector2)

    assert dot_product == expected