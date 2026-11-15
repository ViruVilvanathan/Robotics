# Atlas architecture and extension contracts

## Components

```text
JSON config -> SimulationWorld -> RobotAgent[] -> MachineManager
                       |                 |-> GoToGoalController
                       |                 |-> MotionUpdate -> Pose
                       |                 |-> SafetyManager / StateMachine
                       |-> ObstacleMap
                       |-> snapshot() -> CLI / renderer / future adapters
```

Each `RobotAgent` owns pose, goal, radius, motion limits, mission manager, status and trajectory. `SimulationWorld` owns the map, time, update order and collision policy. `ObstacleMap` owns geometry and swept-path checks. Rendering and config parsing are separate from stepping.

## API contracts

- `ObstacleMap.from_dict(data)`, `.from_json(path)`, `.collides(x,y,radius)`, `.path_clear(x0,y0,x1,y1,radius,resolution)`.
- `RobotAgent.from_dict(data)`: creates pose and enters AUTO with a go-to-goal mission.
- `SimulationWorld.from_dict(data)`, `.step()`, `.run(steps)`, `.snapshot()`.
- `python -m atlas.sim.cli --config FILE [--headless] [--steps N] [--save FILE]`.

## Safety and determinism

All positions and goals are validated against static obstacles at initialization. A swept sample check catches most obstacle crossings at the configured 0.05 m sampling resolution. Inter-agent checks compare moving segments against other robots' current positions; sequential stepping is deterministic but not physically simultaneous. Collisions cause a stop and a navigable-path fault. No recovery planner is implemented. Faults are not automatically reset.

## Future Peekabot seam

A future perception adapter can consume `snapshot()` and publish timestamped observations containing frame_id, robot_id, position estimate, confidence and visibility state. Do not import Peekabot into the core world; use an adapter package and preserve ground-truth separation from estimated perception state.
