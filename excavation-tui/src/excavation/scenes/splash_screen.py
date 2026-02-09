from time import sleep

from rich.text import Text
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

from widgets.logo import logo

class SplashScreen(Screen):
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
            yield Static(Text.from_ansi("\n".join(logo)), expand=False, id="logo")
            yield Label("A Horror Game by Rupnil Codes")
    def fade_and_switch(self):
        self.set_timer(
            2.5,
            lambda: self.screen.styles.animate(
                "opacity", value=0.0, duration=2,
                on_complete=lambda: self.app.switch_screen("new_game")
            )
        )



    def on_mount(self) -> None:
        self.screen.styles.opacity = 0
        self.screen.styles.animate(
            "opacity", value=1.0, duration=1.5,
            on_complete=self.fade_and_switch()
        )
