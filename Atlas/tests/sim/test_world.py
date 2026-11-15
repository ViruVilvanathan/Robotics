import math
import pytest
from atlas.sim.maps import ObstacleMap
from atlas.sim.world import SimulationWorld

def config():
    return {"dt": 0.1, "map": {"width": 10, "height": 10, "obstacles": []},
            "robots": [{"name": "a", "start": [1, 1], "goal": [3, 1]},
                       {"name": "b", "start": [1, 5], "goal": [3, 5]}]}

def test_map_geometry_and_boundary():
    m = ObstacleMap(10, 10, [{"type": "circle", "x": 5, "y": 5, "radius": 1},
                            {"type": "rectangle", "x": 1, "y": 1, "width": 1, "height": 2}])
    assert m.collides(5, 5)
    assert m.collides(1.5, 2)
    assert m.collides(-1, 2)
    assert not m.collides(8, 8)
    assert not m.path_clear(4, 5, 6, 5, 0.1)

def test_bad_map_rejected():
    with pytest.raises(ValueError):
        ObstacleMap(-1, 5)
    with pytest.raises(ValueError):
        ObstacleMap(10, 10, [{"type": "triangle"}])

def test_multi_robot_progress_and_snapshot():
    world = SimulationWorld.from_dict(config())
    before = world.snapshot()
    world.run(15)
    after = world.snapshot()
    assert after["time"] == pytest.approx(1.5)
    assert len(after["robots"]) == 2
    assert all(a["x"] > b["x"] for a, b in zip(after["robots"], before["robots"]))
    assert all(r.manager.mission_running for r in world.robots)

def test_reaches_goal_and_stops_mission():
    cfg = config()
    cfg["robots"] = [cfg["robots"][0]]
    world = SimulationWorld.from_dict(cfg)
    world.run(300)
    assert world.robots[0].status == "reached"
    assert not world.robots[0].manager.mission_running

def test_obstacle_blocks_and_estops():
    cfg = config()
    cfg["robots"] = [cfg["robots"][0]]
    cfg["map"]["obstacles"] = [{"type": "rectangle", "x": 2, "y": 0, "width": 0.3, "height": 3}]
    world = SimulationWorld.from_dict(cfg)
    world.run(100)
    assert world.robots[0].status == "blocked"
    assert world.robots[0].manager.safety_manager.estop_engaged

def test_invalid_start_and_duplicate_names():
    cfg = config()
    cfg["robots"][1]["name"] = "a"
    with pytest.raises(ValueError):
        SimulationWorld.from_dict(cfg)
    cfg["robots"][1]["name"] = "b"
    cfg["robots"][0]["start"] = [-1, 1]
    with pytest.raises(ValueError):
        SimulationWorld.from_dict(cfg)

def test_safety_fault_stops_robot():
    world = SimulationWorld.from_dict(config())
    world.robots[0].manager.safety_manager.power_status = False
    world.step()
    assert world.robots[0].status == "stopped_safety"
    assert world.robots[0].manager.safety_manager.estop_engaged

def test_deterministic_replay():
    a, b = SimulationWorld.from_dict(config()), SimulationWorld.from_dict(config())
    assert a.run(40) == b.run(40)
