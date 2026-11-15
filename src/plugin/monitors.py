"""Every DDC/CI call goes through here so the rest of the plugin can run without real monitors."""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def get_monitors() -> list:
    from monitorcontrol import get_monitors

    return get_monitors()


def get_luminance(monitor) -> Optional[int]:
    from monitorcontrol.vcp import VCPError

    try:
        with monitor:
            return monitor.get_luminance()
    except VCPError:
        logger.warning("Could not read brightness over DDC/CI", exc_info=True)
        return None


def set_luminance(monitor, brightness: int) -> None:
    from monitorcontrol.vcp import VCPError

    try:
        with monitor:
            monitor.set_luminance(brightness)
    except VCPError:
        logger.warning("Could not set brightness over DDC/CI", exc_info=True)
