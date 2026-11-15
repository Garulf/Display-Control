from typing import List, Optional

from pyflowlauncher import Plugin, Result

import monitors

ICON = "icon.png"
BRIGHTNESS_ICON = "brightness.png"
BRIGHTNESS_STEPS = [100, 75, 50, 25, 0]

plugin = Plugin()


@plugin.on_method
def query(query: str) -> List[Result]:
    results = []
    for index, monitor in enumerate(monitors.get_monitors()):
        title = f"Monitor {index + 1}"
        if query.lower() in title.lower():
            luminance = monitors.get_luminance(monitor)
            brightness = "unavailable" if luminance is None else luminance
            results.append(Result(title=title, subtitle=f"Brightness: {brightness}", icon=ICON, context_data=[index]))
    if len(results) > 1:
        results.append(Result(title="All Monitors", icon=ICON, context_data=[None]))
    return results


@plugin.on_method
def context_menu(data) -> List[Result]:
    if not data:
        return []
    index = data[0]
    return [
        Result(
            title=f"{step}%",
            subtitle=f"Set brightness to {step}%",
            icon=BRIGHTNESS_ICON,
        ).add_action(set_luminance, parameters=[step, index])
        for step in BRIGHTNESS_STEPS
    ]


@plugin.on_method
def set_luminance(brightness: int, index: Optional[int] = None) -> None:
    found = monitors.get_monitors()
    targets = found if index is None else [found[index]]
    for monitor in targets:
        monitors.set_luminance(monitor, brightness)
