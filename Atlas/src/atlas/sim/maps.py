"""2D circular/rectangular obstacle maps, loaded from JSON."""
import json
import math
from pathlib import Path

class ObstacleMap:
    def __init__(self, width: float, height: float, obstacles=None):
        self.width, self.height = float(width), float(height)
        if not (math.isfinite(self.width) and math.isfinite(self.height) and self.width > 0 and self.height > 0):
            raise ValueError("Map dimensions must be positive and finite")
        self.obstacles = list(obstacles or [])
        for o in self.obstacles:
            if o.get("type") == "circle":
                if not all(k in o for k in ("x", "y", "radius")) or o["radius"] <= 0:
                    raise ValueError("Invalid circle")
            elif o.get("type") == "rectangle":
                if not all(k in o for k in ("x", "y", "width", "height")) or o["width"] <= 0 or o["height"] <= 0:
                    raise ValueError("Invalid rectangle")
            else:
                raise ValueError("Unknown obstacle type")
            if not all(isinstance(v, (int, float)) and math.isfinite(v) for k, v in o.items() if k != "type"):
                raise ValueError("Obstacle values must be finite numbers")

    @classmethod
    def from_dict(cls, data):
        return cls(data["width"], data["height"], data.get("obstacles", []))

    @classmethod
    def from_json(cls, path):
        return cls.from_dict(json.loads(Path(path).read_text()))

    def collides(self, x: float, y: float, radius: float = 0.0) -> bool:
        if not all(math.isfinite(v) for v in (x, y, radius)) or radius < 0:
            raise ValueError("Invalid collision query")
        if x - radius < 0 or y - radius < 0 or x + radius > self.width or y + radius > self.height:
            return True
        for o in self.obstacles:
            if o["type"] == "circle":
                if math.hypot(x - o["x"], y - o["y"]) < radius + o["radius"]:
                    return True
            else:
                nearest_x = max(o["x"], min(x, o["x"] + o["width"]))
                nearest_y = max(o["y"], min(y, o["y"] + o["height"]))
                if math.hypot(x - nearest_x, y - nearest_y) < radius:
                    return True
                if radius == 0 and o["x"] <= x <= o["x"] + o["width"] and o["y"] <= y <= o["y"] + o["height"]:
                    return True
        return False

    def path_clear(self, x0, y0, x1, y1, radius=0.0, resolution=0.05):
        if resolution <= 0:
            raise ValueError("Resolution must be positive")
        steps = max(1, math.ceil(math.hypot(x1 - x0, y1 - y0) / resolution))
        return all(not self.collides(x0 + (x1-x0)*i/steps, y0 + (y1-y0)*i/steps, radius) for i in range(steps+1))
