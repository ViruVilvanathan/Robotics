"""Integration tests for the real local HTTP simulation API."""
import json
import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pytest
from atlas.sim.web import scene
from atlas.sim.world import SimulationWorld


def config():
    return {"dt": 0.1, "map": {"width": 8, "height": 8,
            "obstacles": [{"type": "circle", "x": 4, "y": 4, "radius": 0.5}]},
            "robots": [{"name": "a", "start": [1, 1], "goal": [6, 1]}]}


def test_scene_contains_map_trajectories_and_safety():
    world = SimulationWorld.from_dict(config())
    before = scene(world)
    assert before["map"]["obstacles"][0]["type"] == "circle"
    assert before["robots"][0]["trajectory"] == [[1.0, 1.0]]
    assert before["robots"][0]["safety"]["navigable_path"] is True
    world.step()
    after = scene(world)
    assert after["time"] == pytest.approx(0.1)
    assert len(after["robots"][0]["trajectory"]) == 2
    assert after["robots"][0]["x"] != before["robots"][0]["x"]


def test_scene_is_json_serializable():
    json.dumps(scene(SimulationWorld.from_dict(config())), allow_nan=False)


@contextmanager
def running_server(tmp_path):
    cfg = tmp_path / "world.json"
    cfg.write_text(json.dumps(config()))
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    process = subprocess.Popen(
        [sys.executable, "-m", "atlas.sim.web", "--config", str(cfg), "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(80):
            if process.poll() is not None:
                raise AssertionError("Server exited before becoming ready")
            try:
                with urlopen(base + "/api/state", timeout=0.3):
                    break
            except (URLError, TimeoutError):
                time.sleep(0.05)
        else:
            raise AssertionError("Server did not become ready")
        yield base
    finally:
        process.terminate()
        try:
            process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=3)


def request(base, path, data=None):
    payload = None if data is None else json.dumps(data).encode()
    req = Request(base + path, data=payload,
                  headers={"Content-Type": "application/json"} if data is not None else {})
    with urlopen(req, timeout=3) as response:
        return response.status, response.read(), response.headers.get("Content-Type")


def test_http_ui_and_simulation_lifecycle(tmp_path):
    with running_server(tmp_path) as base:
        status, html, mime = request(base, "/")
        assert status == 200 and "text/html" in mime
        assert b"Mission Control" in html
        assert b"/api/step" in html

        _, body, _ = request(base, "/api/state")
        initial = json.loads(body)
        assert initial["time"] == 0
        assert len(initial["robots"]) == 1
        assert initial["map"]["obstacles"][0]["type"] == "circle"

        _, body, _ = request(base, "/api/step", {"steps": 3})
        moved = json.loads(body)
        assert moved["time"] == pytest.approx(0.3)
        assert moved["robots"][0]["x"] > initial["robots"][0]["x"]
        assert len(moved["robots"][0]["trajectory"]) == 4

        _, body, _ = request(base, "/api/goal", {"name": "a", "x": 2, "y": 2})
        changed = json.loads(body)
        assert changed["robots"][0]["goal"] == [2, 2]

        for invalid in ({"name": "a", "x": 4, "y": 4},
                        {"name": "missing", "x": 2, "y": 2},
                        {"name": "a", "x": 100, "y": 2}):
            with pytest.raises(HTTPError) as exc:
                request(base, "/api/goal", invalid)
            assert exc.value.code == 400

        with pytest.raises(HTTPError) as exc:
            request(base, "/api/step", {"steps": 1000000})
        assert exc.value.code == 400

        _, body, _ = request(base, "/api/reset", {})
        reset = json.loads(body)
        assert reset["time"] == 0
        assert reset["robots"][0]["goal"] == [6, 1]
        assert len(reset["robots"][0]["trajectory"]) == 1
