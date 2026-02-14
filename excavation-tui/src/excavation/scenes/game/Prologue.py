from asyncio import sleep

from textual import work, events
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

DIALOGUES = [
    "January 1344 CE,\nPetén, Postclassic Maya.",
    "Cold breeze rolls across Lake P. Itza",
    "Cadmael does not slow",
    "Hold \[SPACE] to run through woods.",
    # IF PLAYER KEEPS HOLDING SPACE FOR >5sec
    "Your lungs burn, You stop and gasp for breath.",
    # IF PLAYER HOLDS SPACE FOR <5sec
    "You're exhausted. You stop among the trees.",
    "The air seems quiet. Suspiciously quiet.",
    "Something moves. Press \[ANY KEY]",
    # IF ANY KEY in <3s:
    "Cadmael almost managed to move. Almost.",
    # IF ANY KEY in >3s:
    "Cadmael never saw it coming.",
    "You feel cold and heavy. You kneel down.",
    "A tall figure retrieves it from your robe.",
    "Press \[SPACE] to look up.",
    "You look up to see the glimmer of...",
    "Your vision fades.",
    "The cold waters closes over you. Press \[ENTER]",
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
        # opacity: 0;
    }
    
    .stamina {
        text-align: center;
        margin: 1;
    }
    
    """

    ENTER = False
    SPACE = False

    dialogue = Label("", id="dialogue")
    health = Label(" Health: ████████", classes="stamina")
    stamina = Label("Stamina: █████", classes="stamina")

    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            with Container(id="dialogue-container"):
                yield self.dialogue
            with Container(id="sidebar-dock"):
                yield self.health
                yield self.stamina

    def on_mount(self) -> None:
        self.screen.styles.opacity = 0
        self.call_later(self.sequence)

    async def wait(self, sec: float) -> None:
        loops = int(sec/0.05)
        for i in range(loops):
            if not self.ENTER:
                await sleep(0.05)
            else:
                self.ENTER = False
                break
        self.ENTER = False

    async def typewrite(self, widget: Label, text: str) -> None:
        text = list(text)
        masked = []

        for char in text:
            if char == "\n":
                masked.append("\n")
            else:
                masked.append(" ")

        for i in range(len(text)):
            if not self.ENTER:
                masked[i] = text[i]
                widget.update("".join(masked))
                await sleep(0.05)
        widget.update("".join(text))
        self.ENTER = False


    @work
    async def sequence(self)-> None:
        self.screen.styles.animate(
            "opacity", value=1.0, duration=1.5,
        )
        await sleep(1.5)
        self.screen.refresh(recompose=True)

        for i in range(len(DIALOGUES)):
            await self.typewrite(self.dialogue, DIALOGUES[i])
            await self.wait(5)

    def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.ENTER = True
