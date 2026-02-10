from rich.text import Text
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

from widgets import FlashMessage, logo, username
from config import AUTHOR

class SplashScreen(Screen):
    CSS = """
    FlashMessage {
        layer: overlay;
        position: absolute;
        width: 100%;
        height: 100%;
        align: center middle;
        color: rgb(255,50,50);
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            yield Static(Text.from_ansi("\n".join(logo)), expand=False, id="logo")
            yield Label(f"A Game by {AUTHOR} <3")

    def flash_unmount_function(self):
        self.set_timer(
            1,
            lambda: self.screen.styles.animate(
                "opacity", value=0.0, duration=1.5,
                on_complete=lambda: self.app.switch_screen("new_game"),
            )
        )

    def flash_message(self):
        self.set_timer(
            1.25,
            lambda: self.mount(
                FlashMessage(
                    self.flash_unmount_function,
                    1.5,
                    f"[reverse][b][i]Help me, {username()}[/i][/b][/reverse]\n[dim][i]Save, me.[/i][/]"
                )
            ),
        )

    def on_mount(self) -> None:
        self.screen.styles.opacity = 0
        self.screen.styles.animate(
            "opacity", value=1.0, duration=1.5,
            on_complete=self.flash_message,
        )

