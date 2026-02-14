from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

from widgets import username, glitch_text

class NewGame(Screen):
    CSS = """
    #wrapper {
        width: auto;
        height: auto;
        align: center middle;
        layout: vertical;
    }
    
    #help {
        color: rgb(255,50,50);
    }
    """

    label = None
    message1 = None
    message2 = None
    newline = None
    final_message = None

    # def compose(self) -> ComposeResult:
    #     with Container(id="wrapper"):
    #         self.label = Label(f"[reverse][b][i]Help me, {username()}[/i][/b][/reverse]\n[dim][i]Save, me.[/i][/]", id="help")
    #         yield self.label

    def on_mount(self) -> None:
        self.app.switch_screen("prologue")