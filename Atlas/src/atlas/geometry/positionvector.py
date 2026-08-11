import math

class Position:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y}, z={self.z})"

    def vector_to(self, other: 'Position') -> 'Vector':
        return Vector(other.x - self.x, other.y - self.y, other.z - self.z)

    def distance_to(self, other: 'Position') -> float:
        return self.vector_to(other).magnitude()


class Vector:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    def magnitude(self) -> float:
        return math.hypot(self.x, self.y, self.z)

    def normalized(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero vector.")

        return Vector(
        self.x / magnitude,
        self.y / magnitude,
        self.z / magnitude
        )
    def dot(self, other: 'Vector') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

