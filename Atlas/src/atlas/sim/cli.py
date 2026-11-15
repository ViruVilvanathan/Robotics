"""Run: python -m atlas.sim.cli --config examples/two_robots.json"""
import argparse
import json
from pathlib import Path
from .world import SimulationWorld

def main(argv=None):
    parser = argparse.ArgumentParser(description="Atlas multi-robot simulator")
    parser.add_argument("--config", required=True, help="JSON world configuration")
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--save", help="Save final snapshot as JSON")
    args = parser.parse_args(argv)
    config = json.loads(Path(args.config).read_text())
    world = SimulationWorld.from_dict(config)
    if args.headless:
        result = world.run(args.steps)
        print(json.dumps(result, indent=2))
    else:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle, Rectangle
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.set_xlim(0, world.map.width)
        ax.set_ylim(0, world.map.height)
        ax.set_title("Atlas multi-robot simulation")
        for o in world.map.obstacles:
            if o["type"] == "circle":
                ax.add_patch(Circle((o["x"], o["y"]), o["radius"], color="gray"))
            else:
                ax.add_patch(Rectangle((o["x"], o["y"]), o["width"], o["height"], color="gray"))
        artists = []
        for r in world.robots:
            dot, = ax.plot([], [], "o", label=r.name)
            trail, = ax.plot([], [], "-", alpha=0.45)
            ax.plot(r.goal.x, r.goal.y, "x", color=dot.get_color())
            artists.append((dot, trail))
        ax.legend()
        for _ in range(args.steps):
            if not plt.fignum_exists(fig.number):
                break
            world.step()
            for r, (dot, trail) in zip(world.robots, artists):
                dot.set_data([r.pose.position.x], [r.pose.position.y])
                trail.set_data([p[0] for p in r.trajectory], [p[1] for p in r.trajectory])
            fig.canvas.draw_idle()
            plt.pause(world.dt)
        result = world.snapshot()
        print(json.dumps(result, indent=2))
        plt.show()
    if args.save:
        Path(args.save).write_text(json.dumps(result, indent=2) + "\n")

if __name__ == "__main__":
    main()
