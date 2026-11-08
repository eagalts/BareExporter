import json
from pathlib import Path

from runners.thermal import parse_thermal

FIXTURES = Path(__file__).parent / "fixtures"

def _init():
    with open(FIXTURES / "thermal.json") as f:
        data = json.load(f)
        thermal, fans = parse_thermal(data)
        cpu1 = [sensor for sensor in thermal if sensor["Name"] == "CPU1 Temp"]
        return thermal, fans, cpu1

def test_thermal():
    thermal, _, _ = _init()
    assert len(thermal) == 4

def test_fans():
    _, fans, _ = _init()
    assert len(fans) == 14

def test_cpu_item():
    _, _, cpu1 = _init()
    assert len(cpu1) == 1

def test_cpu_instance():
    _, _, cpu1 = _init()
    assert isinstance(cpu1[0]["Value"], (int, float))