import json
from atlas.sim.cli import main

def test_headless_cli(tmp_path, capsys):
    config = {"map": {"width": 6, "height": 6, "obstacles": []},
              "robots": [{"name": "one", "start": [1, 1], "goal": [3, 1]}]}
    path = tmp_path / "world.json"
    output = tmp_path / "result.json"
    path.write_text(json.dumps(config))
    main(["--config", str(path), "--steps", "10", "--headless", "--save", str(output)])
    assert json.loads(output.read_text())["robots"][0]["x"] > 1
    assert "one" in capsys.readouterr().out
