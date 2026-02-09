from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

class NewGame(Screen):
    CSS = """
    #wrapper {
        width: auto;
        height: auto;
        align: center middle;
        layout: vertical;
    }
    """
    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            yield Label("NEW GAME SCENE")

    def on_mount(self) -> None:
        self.screen.styles.opacity = 0
        self.screen.styles.animate("opacity", value=1.0, duration=1)
