from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import App, ComposeResult

from textual import events

from .utils.cli import logo
from rich.text import Text

class MainMenu(Screen):
    CSS = """

"""
    selected = 0
    menu_items = [
        "New Game",
        "Load Save",
        "Settings",
        "Preference",
        "Quit",
    ]

    def compose(self) -> ComposeResult:
        yield Static(Text.from_ansi("\n".join(logo)), expand=False)

        for i in range(len(self.menu_items)):
            if self.selected == i:
                yield Label("[b] ►[/b] " + self.menu_items[i])
            else:
                yield Label("  " + self.menu_items[i])

    # def on_mount(self) -> None:
    #     self.screen.styles.background = "darkblue"
    #     self.push_screen(IntroScreen())