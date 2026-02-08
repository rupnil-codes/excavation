from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Container
from textual import on

class VictoryScreen(ModalScreen): #gemini css
    CSS = """
    VictoryScreen {
        align: center middle;
        background: 0%; 
    }
    #victory-box {
        width: 50;
        height: auto; /* changed to auto so it grows with the extra label */
        border: double yellow;
        background: black;
        align: center middle;
        text-align: center;
        padding-bottom: 1;
    }
    Label {
        margin: 1 0;
        color: white;
    }
    /* NEW CSS for Level Up Text */
    #lvl-up {
        color: #00ff00; 
        text-style: bold;
    }
    Button {
        margin-top: 2;
        background: #ff9900;
        color: black;
    }
    """

    def __init__(self, exp_gained: int, gold_gained: int, leveled_up: bool = False):
        super().__init__()
        self.exp = exp_gained
        self.gold = gold_gained
        self.leveled_up = leveled_up

    def compose(self) -> ComposeResult:
        with Container(id="victory-box"):
            yield Label("VICTORY!", id="title")
            yield Label(f"* You won {self.exp} EXP and {self.gold} Gold.")
            
            #check if lvl up new!
            if self.leveled_up:
                yield Label(" Your LOVE increased!", id="lvl-up")

            yield Button("Continue", id="btn-continue")

    @on(Button.Pressed)
    def handle_continue(self, event: Button.Pressed):
        self.dismiss(True)