import os

from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.app import ComposeResult

from textual import events, on

from config import VERSION, RELEASE
from widgets import type_sfx, menu, fade_out

from widgets import logo
from rich.text import Text

class MainMenu(Screen):
    CSS = """
    /* NEW: This holds the text and the box together */
    #wrapper {
        layout: vertical;
    }

    #choice_text {
        text-align: center;
        color: yellow;
        margin-bottom: 1;
    }

    #menu-box {
        width: 57;
        height: auto;
        border: panel white;
        padding: 1 1 0 1;
        margin: 0 0 0 0;
        # border-subtitle-style: "Centered Subtitle";
        border-subtitle-align: right;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
        background: transparent;
        color: white;
        border: none;
        text-style: none;
        text-align: center;
    }
    
    Button:focus {
        background: white;
        color: #0d0d0d;
        text-style: bold;
    }
    
    Button:hover {
        background: #222222;
        color: white;
    }
    
    Button.-disabled {
        color: #444444;
        background: black;
    }
"""

    index = None
    buttons = None

    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            yield Static(Text.from_ansi("\n".join(logo)), expand=False, id="logo")

            with Container(id="menu-box"):
                yield Button("New Game", id="new")
                yield Button("Load Save", id="load")
                yield Button("Settings", id="settings")
                yield Button("Quit", id="quit")


    def on_mount(self) -> None:
        menu()
        self.call_after_refresh(
            lambda: self.query_one("#new").focus()
        )

        self.query_one("#menu-box").border_title = "[b]Main Menu[/b]"
        self.query_one("#menu-box").border_subtitle = f"{VERSION}-{RELEASE}"

        self.buttons = self.query("#menu-box Button")
        self.index = 0
        self.buttons[self.index].focus()

        # self.push_screen(IntroScreen())

    @on(Button.Pressed)
    def handle_menu_click(self, event: Button.Pressed):
        # TODO:
        if event.button.id == "new":
            type_sfx()
            fade_out(2)
            self.screen.styles.animate(
                "opacity", value=0.0, duration=2,
                on_complete=lambda: self.app.switch_screen("splash_screen")
            )


        if event.button.id == "load":
            type_sfx()
            pass

        if event.button.id == "settings":
            type_sfx()
            pass

        if event.button.id == "quit":
            type_sfx()
            self.app.exit()


    def _on_key(self, event: events.Key) -> None:
        if event.key in ("up", "w"):
            self.index = (self.index - 1) % len(self.buttons)
            type_sfx()
            self.buttons[self.index].focus()
        elif event.key in ("down", "s"):
            self.index = (self.index + 1) % len(self.buttons)
            type_sfx()
            self.buttons[self.index].focus()
