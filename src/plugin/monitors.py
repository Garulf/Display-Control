"""Every DDC/CI call goes through here so the rest of the plugin can run without real monitors."""


def get_monitors() -> list:
    from monitorcontrol import get_monitors

    return get_monitors()


def get_luminance(monitor) -> int:
    with monitor:
        return monitor.get_luminance()


def set_luminance(monitor, brightness: int) -> None:
    with monitor:
        monitor.set_luminance(brightness)
