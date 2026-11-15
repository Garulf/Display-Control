import pytest

import monitors


class FakeMonitor:
    def __init__(self, luminance=50):
        self.luminance = luminance
        self.open = False
        self.calls = []

    def __enter__(self):
        self.open = True
        return self

    def __exit__(self, *exc):
        self.open = False
        return False

    def get_luminance(self):
        assert self.open, "monitorcontrol calls must run inside the context manager"
        self.calls.append(("get_luminance",))
        return self.luminance

    def set_luminance(self, value):
        assert self.open, "monitorcontrol calls must run inside the context manager"
        self.calls.append(("set_luminance", value))
        self.luminance = value


@pytest.fixture
def displays(monkeypatch):
    found = [FakeMonitor(80), FakeMonitor(30)]
    monkeypatch.setattr(monitors, "get_monitors", lambda: list(found))
    return found
