# Atlas — Modular Robotics Simulation Platform

Atlas is a Python 3.11+ robotics sandbox with geometry, rigid-body pose transforms, guidance, kinematics, operational state, safety and a deterministic multi-robot 2D simulation.

## Quick start (macOS)

```bash
cd Atlas
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -v
python -m atlas.sim.cli --config examples/two_robots.json
```

For a terminal-only run:

```bash
python -m atlas.sim.cli --config examples/two_robots.json --headless --steps 500 --save snapshot.json
```

The older interactive single-robot demo remains available with `python -m atlas.simulation`.

## Architecture

- `geometry.positionvector`: `Position(x,y,z)`, `Vector(x,y,z)`; displacement, distance, magnitude, normalization and dot product.
- `orientation.rotations`: 3D rotation matrices, body/world rotations in radians.
- `orientation.pose`: body/world point and vector transforms.
- `guidance.goalcontroller`: proportional go-to-goal linear and angular commands.
- `kinematics.motionupdate`: forward-integrate planar commands into a new pose.
- `state_machine`: OFF, IDLE, MANUAL, AUTO, E_STOP transitions.
- `safety_manager`: E-stop and subsystem-health motion gate.
- `machine_manager`: per-robot mission lifecycle and safety coordination.
- `sim.maps`: bounded 2D world with circles and axis-aligned rectangles.
- `sim.world`: independent agents, fixed timestep, collision checks, deterministic snapshots.
- `sim.cli`: JSON world loading, headless and Matplotlib visualization.

## World configuration

See [examples/two_robots.json](examples/two_robots.json). Supply your own file via `--config path/to/world.json`.

Top-level: `dt` (seconds), `goal_tolerance` (meters), `map`, `robots`.
Map: `width`, `height`, `obstacles`. Obstacles support `{"type":"circle","x":5,"y":5,"radius":1}` or `{"type":"rectangle","x":2,"y":3,"width":1,"height":2}`.
Robots: `name`, `start:[x,y]`, `goal:[x,y]`, optional `heading` (radians), `radius`, `max_speed`, `max_turn_rate`.
Coordinates are meters; +x right, +y up, positive heading counterclockwise. Commands are body-frame linear speed (m/s) and yaw rate (rad/s).

## Simulation contract and limitations

`SimulationWorld.from_dict(config)`, `.step()`, `.run(steps)`, and `.snapshot()` form the stable integration seam. Snapshot includes simulation time and robot name, x/y, heading, goal and status. These JSON-compatible snapshots are intended for future adapters, **not a current Peekabot integration**.

Each agent owns its own `MachineManager`, safety state and pose. A blocked step triggers a navigable-path fault and E-stop. The controller is reactive go-to-goal, **not a global planner**: robots stop at obstacles rather than finding alternate routes. Robot updates are sequential, not a simultaneous multi-agent physics solver. There is no sensor simulation, dynamic obstacle planning, physics engine, ROS 2 bridge, or collision-certified safety guarantee. This is a software learning/test environment, not deployable vehicle control.

## Tests

`python -m pytest -v` runs existing geometry, pose, guidance and kinematics tests alongside new world and CLI tests. Headless mode is suitable for CI.

## Next milestones

Grid maps/occupancy maps, A*/RRT path planning, dynamic obstacles, synchronized robot arbitration, sensor observations, event logs and replay, ROS 2 adapter, and later a Peekabot observation adapter. Keep external perception pipelines separate from world dynamics.
