from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Static
from textual import on
from textual.containers import Container
from assets.save_manager import load_game, has_save_file, SAVE_FILE
import json
import os
import time
from assets.music_manager import play_music

class TitleScreen(Screen):
    BINDINGS = [
        ("up", "app.focus_previous", "Move Up"),
        ("down", "app.focus_next", "Move Down")
    ]
    CSS = """
    TitleScreen {
        align: center middle; /* Center the wrapper */
        background: black;
    }
    
    /* NEW: This holds the text and the box together */
    #wrapper {
        width: auto;
        height: auto;
        align: center middle;
        layout: vertical;
    }

    #choice_text {
        text-align: center;
        color: yellow;
        margin-bottom: 2;
        text-style: bold;
    }

    #menu-box {
        width: 30;
        height: auto;
        border: double yellow;
        padding: 1;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
        background: black;
        color: white;
        border: none;
        text-align: center;
    }
    
    Button:focus {
        background: white;
        color: black;
        text-style: bold;
    }
    
    Button.-disabled {
        color: #444444;
        background: black;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            
            choice_text = "What would you like to do,\nHuman?"
            yield Static(choice_text, id="choice_text")
            
            with Container(id="menu-box"):
                yield Button("LOAD GAME", id="btn-load")
                yield Button("NEW GAME", id="btn-new")
                yield Button("QUIT", id="btn-quit")
                yield Button("DELETE SAVE", id="btn-delete")
            
    def on_mount(self):
            btn_cont = self.query_one("#btn-load")
            btn_cont.focus()
            play_music("menu")
    
    @on(Button.Pressed)
    def handle_menu_click(self, event: Button.Pressed):
        
        if event.button.id == "btn-load":
            if load_game():
                from screens.map_screen import MapScreen
                self.app.push_screen(MapScreen())
        elif event.button.id == "btn-new":
            from screens.intro_screen import IntroScreen
            self.app.push_screen(IntroScreen())
        elif event.button.id == "btn-quit":
            self.app.exit()
        elif event.button.id == "btn-delete":
            os.remove(SAVE_FILE)
            self.query_one("#choice_text").update("Save file erased.\nThere is no going back.\n Game will be exited...")
            self.set_timer(1.5, self.app.exit)