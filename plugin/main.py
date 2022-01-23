from flox import Flox

from monitorcontrol import get_monitors

BRIGHTNESS_STEPS = [100, 75, 50, 25, 0]

class DisplayControl(Flox):

    def __init__(self):
        super().__init__(debug=True)
        self.monitors = []
        for monitor in get_monitors():
            self.monitors.append(monitor)

    def query(self, query):
        for idx, monitor in enumerate(self.monitors):
            title = f"Monitor {idx + 1}"
            if query.lower() in title.lower():
                with monitor:
                    luminance = monitor.get_luminance()
                    self.add_item(
                        title=title,
                        subtitle=f"Brightness: {luminance}",
                        icon=self.icon,
                        context=[idx]
                    )
        if len(self._results) > 1:
            self.add_item(
                title="All Monitors",
                icon=self.icon,
                context=[None]
            )


    def context_menu(self, data):
        index = data[0]
        for step in BRIGHTNESS_STEPS:
            self.add_item(
                title=f"{step}%",
                subtitle=f"Set brightness to {step}%",
                icon='./brightness.jpg',
                method=self.set_luminance,
                parameters=[step, index]
            )

    def set_luminance(self, brightness, index=None):
        if index is None:
            for monitor in self.monitors:
                with monitor:
                    monitor.set_luminance(brightness)
        else:
            with self.monitors[index] as monitor:
                self.logger.debug(monitor.get_luminance())
                monitor.set_luminance(brightness)

    def set_contrast(self, contrast, index=None):
        if index is None:
            for monitor in self.monitors:
                with monitor:
                    monitor.set_contrast(contrast)
        else:
            with self.monitors[index] as monitor:
                monitor.set_contrast(contrast)

    def set_input(self, input, index):
        with self.monitors[index] as monitor:
            monitor.set_input_source(input)

if __name__ == "__main__":
    DisplayControl()
