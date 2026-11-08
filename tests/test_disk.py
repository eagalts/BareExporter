import json
from pathlib import Path

from runners.disk import parse_drive_links, parse_drive

FIXTURES = Path(__file__).parent / "fixtures"


def load(name):
    with open(FIXTURES / name) as f:
        return json.load(f)


def test_drive_links_count():
    links = parse_drive_links(load("storage.json"))
    assert len(links) == 2


def test_drive_links_are_paths():
    links = parse_drive_links(load("storage.json"))
    assert all(link.startswith("/redfish/v1/") for link in links)


def test_drive():
    drive = parse_drive(load("drive.json"))
    assert drive == {
        "Name": "Solid State Disk 0:0",
        "Health": "OK",
        "FailurePredicted": False,
    }