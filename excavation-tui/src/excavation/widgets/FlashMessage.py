from textual.containers import Container
from textual.widgets import Label

from widgets.utils.sounds_manager import glitch_sfx, stop

class FlashMessage(Container):
    def __init__(self, function, time: float, message: str = "Flash Message") -> None:
        super().__init__()
        self.message = message
        self.function = function
        self.time = time

    def compose(self):
        with Container(id="wrapper"):
            yield Label(
                self.message,
                id="flash-text"
            )

    def on_mount(self) -> None:
        glitch_sfx()
        self.set_timer(
            self.time,
            self.remove
        )

    def on_unmount(self) -> None:
        stop()
        self.function()
