"""UI adapter tests: the browser must observe the real Python simulation."""
import json
import threading
from urllib.request import Request, urlopen
from atlas.sim.web import scene, serve
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
    assert after["time"] == 0.1
    assert len(after["robots"][0]["trajectory"]) == 2
    assert after["robots"][0]["x"] != before["robots"][0]["x"]


def test_scene_is_json_serializable():
    json.dumps(scene(SimulationWorld.from_dict(config())), allow_nan=False)
