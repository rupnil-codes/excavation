from textual.containers import Container
from textual.widgets import Label

class FlashMessage(Container):
    def __init__(self, start_function, end_function, time: float, message: str = "Flash Message") -> None:
        super().__init__()
        self.message = message
        self.start_function = start_function
        self.end_function = end_function
        self.time = time

    def compose(self):
        with Container(id="wrapper"):
            yield Label(
                self.message,
                id="flash-text"
            )

    def on_mount(self) -> None:
        self.start_function()
        self.set_timer(
            self.time,
            self.remove
        )

    def on_unmount(self) -> None:
        self.end_function()
