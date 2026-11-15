"""Local browser UI adapter for Atlas's existing planar SimulationWorld.

Run: python -m atlas.sim.web --config examples/two_robots.json
No external Python web framework required.
"""
import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .world import SimulationWorld

HTML = Path(__file__).with_name("viewer.html")


def scene(world):
    state = world.snapshot()
    state["dt"] = world.dt
    state["map"] = {"width": world.map.width, "height": world.map.height,
                    "obstacles": world.map.obstacles}
    for item, agent in zip(state["robots"], world.robots):
        item["radius"] = agent.radius
        item["trajectory"] = [[float(x), float(y)] for x, y in agent.trajectory]
        item["safety"] = {"navigable_path": bool(agent.manager.safety_manager.navigable_path)}
    return state


def serve(config, host="127.0.0.1", port=8765):
    lock = threading.RLock()
    world = SimulationWorld.from_dict(config)

    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, obj):
            body = json.dumps(obj, allow_nan=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if urlparse(self.path).path == "/":
                body = HTML.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif urlparse(self.path).path == "/api/state":
                with lock:
                    self.respond(200, scene(world))
            else:
                self.respond(404, {"error": "Not found"})

        def do_POST(self):
            nonlocal world
            path = urlparse(self.path).path
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > 4096:
                    raise ValueError("Invalid request size")
                data = json.loads(self.rfile.read(length) or b"{}")
                with lock:
                    if path == "/api/step":
                        steps = data.get("steps", 1)
                        if type(steps) is not int or not 1 <= steps <= 20:
                            raise ValueError("steps must be an integer between 1 and 20")
                        world.run(steps)
                    elif path == "/api/reset":
                        world = SimulationWorld.from_dict(config)
                    elif path == "/api/goal":
                        name, x, y = data["name"], float(data["x"]), float(data["y"])
                        from atlas.geometry.positionvector import Position
                        import math
                        if not all(math.isfinite(v) for v in (x, y)):
                            raise ValueError("Goal must be finite")
                        robot = next((r for r in world.robots if r.name == name), None)
                        if robot is None:
                            raise ValueError("Unknown robot")
                        if robot.status != "moving":
                            raise ValueError("Only moving robots can accept a new goal; reset to restart")
                        if world.map.collides(x, y, robot.radius):
                            raise ValueError("Goal is obstructed or outside map")
                        robot.goal = Position(x, y, 0)
                    else:
                        self.respond(404, {"error": "Not found"})
                        return
                    self.respond(200, scene(world))
            except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
                self.respond(400, {"error": str(exc)})

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Atlas simulator: http://{host}:{port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description="Atlas 3D-looking simulator UI")
    parser.add_argument("--config", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    serve(json.loads(Path(args.config).read_text()), args.host, args.port)


if __name__ == "__main__":
    main()
