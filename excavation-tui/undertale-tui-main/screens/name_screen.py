from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Input, Label
from textual.containers import Container
from textual import on
from assets.music_manager import play_music

# IMPORTS
from assets.player_stats import player
from screens.map_screen import MapScreen

class NameScreen(Screen):
    CSS = """
    NameScreen {
        align: center middle;
        background: black;
    }
    #name-container {
        width: 60;
        height: auto;
        border: solid white;
        padding: 2;
        align: center middle;
    }
    Label {
        color: white;
        margin-bottom: 1;
        text-style: bold;
    }
    Input {
        width: 100%;
        border: solid yellow;
        color: yellow;
    }
    """
    
    def on_mount(self):
        play_music("creation")

    def compose(self) -> ComposeResult:
        with Container(id="name-container"):
            yield Label("Name the fallen human:", id="lbl-prompt")
            # 12 max name
            yield Input(placeholder="Type name here...", max_length=12, id="input-name")

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted):
        new_name = event.value.strip()
        
        if not new_name:
            self.query_one("#lbl-prompt").update("[red]Name cannot be empty![/red]")
            return

        player["name"] = new_name

        self.app.switch_screen(MapScreen())