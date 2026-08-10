import math

class Position:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y})"

class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"

    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def normalized(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero vector.")

        return Vector(
        self.x / magnitude,
        self.y / magnitude,
        )