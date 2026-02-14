from time import sleep

from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

DIALOGUES = [
    "January 1344 CE,\nPetén, Postclassic Maya.",
    "Cold breeze rolls across Lake P. Itza",
    "Cadmael does not slow",
    "Hold [SPACE] to run through woods.",
    # IF PLAYER KEEPS HOLDING SPACE FOR >5sec
    "Your lungs burn, You stop and gasp for breath.",
    # IF PLAYER HOLDS SPACE FOR <5sec
    "You're exhausted. You stop among the trees.",
    "The air seems quiet. Suspiciously quiet.",
    "Something moves. Press [ANY KEY]",
    # IF ANY KEY in <3s:
    "Cadmael almost managed to move. Almost.",
    # IF ANY KEY in >3s:
    "Cadmael never saw it coming.",
    "You feel cold and heavy. You kneel down.",
    "A tall figure retrieves it from your robe.",
    "Press [SPACE] to look up.",
    "You look up to see the glimmer of...",
    "Your vision fades.",
    "The cold waters closes over you. Press [ENTER]",
    # ENTER does nothing!
    "Is this... the coldness of death?"
]

class Prologue(Screen):
    CSS = """
    #wrapper {
        width: auto;
        height: auto;
        align: center middle;
        layout: horizontal;
    }
    
    #dialogue-container {
        layout: vertical;
        align: center middle;
    }
    
    #sidebar-dock {
        dock: right;
        width: 25%;
        height: 100%;
        background: #b23434;
        align: center middle;
    }
    
    .stamina {
        text-align: center;
        margin: 1;
    }
    
    """

    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            with Container(id="dialogue-container"):
                yield Label(DIALOGUES[0], id="dialogue")
            with Container(id="sidebar-dock"):
                yield Label(" Health: ████████░", classes="stamina")
                yield Label("Stamina: █████░░░░", classes="stamina")

    def func(self):
        stamina = self.query("#stamina")
        stamina.remove()

    def on_mount(self) -> None:
        # self.set_timer(
        #     3,
        #     lambda: self.query_one("#dialogue", Static).update("He;;p"),
        # )
            # sleep(1)

        pass
