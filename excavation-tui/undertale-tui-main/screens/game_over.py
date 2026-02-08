from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Container
from textual import on
from assets.music_manager import play_music

class GameOver(Screen):
    BINDINGS = [
        ("right", "app.focus_next", "Next"),
        ("left", "app.focus_previous", "Previous"),
    ]
    # css = yk
    CSS = """
    GameOver {
        align: center middle;
        background: black;
    }
    
    #game-over-text {
        color: #FF0000; /* Bright Red */
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
    }
    
    #button-container {
        layout: horizontal;
        align: center middle;
        height: 5;
        width: 100%;
    }
    
    Button {
        margin: 0 2;
        background: #330000;
        color: #ff0000;
        border: solid #ff0000;
    }
    
    Button:hover {
        background: #ff0000;
        color: white;
    }
    """
    def compose(self) -> ComposeResult:
        # art by gemini
        art = """
  ________    _____      _____  ___________ _______________   _________________________ 
 /  _____/   /  _  \\    /     \\ \\_   _____/ \\_____  \\   \\ /   /\\_   _____/\\______   \\
/   \\  ___  /  /_\\  \\  /  \\ /  \\ |    __)_   /   |   \\   Y   /  |    __)_  |       _/
\\    \\_\\  \\/    |    \\/    Y    \\|        \\ /    |    \\     /   |        \\ |    |   \\
 \\______  /\\____|__  /\\____|__  /_______  / \\_______  /\\___/   /_______  / |____|_  /
        \\/         \\/         \\/        \\/     Stay \\/ Determined...    \\/         \\/ 
"""
        yield Static(art, id="game-over-text")
        with Container(id = "button-container"):
            yield Button("Retry", id="btn-retry")
            yield Button("Quit", id="btn-quit")
    @on(Button.Pressed)
    def function(self, event: Button.Pressed):
        if event.button.id == "btn-retry":
            self.dismiss(True)
        elif event.button.id == "btn-quit":
            self.dismiss(False)
            
    def on_mount(self):
        play_music("death")