import json
from pathlib import Path

from runners.psu import parse_psu

FIXTURES = Path(__file__).parent / "fixtures"

def test_psu():
    with open(FIXTURES / "power.json") as f:
        data = json.load(f)
    assert parse_psu(data) == [{"Name": "PS1 Status", "State": "OK"}]