from asyncio import sleep

from textual import work, events
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

from config import INFINITE_TIMER, MICRO_SLEEP

DIALOGUES = [
    "January 1344 CE,\nPetén, Postclassic Maya.",
    "Cold breeze rolls across Lake P. Itza",
    "Cadmael does not slow",
    "Hold \\[SPACE] to run through woods.",
    # IF PLAYER KEEPS HOLDING SPACE FOR >5sec
    "Your lungs burn, You stop and gasp for breath.",
    # IF PLAYER HOLDS SPACE FOR <5sec
    "You're exhausted. You stop among the trees.",
    "The air seems quiet. Suspiciously quiet.",
    "Something moves. Press \\[ANY KEY]",
    # IF ANY KEY in <3s:
    "Cadmael almost managed to move. Almost.",
    # IF ANY KEY in >3s:
    "Cadmael never saw it coming.",
    "You feel cold and heavy. You kneel down.",
    "A tall figure retrieves it from your robe.",
    "Press \\[SPACE] to look up.",
    "You look up to see the glimmer of...",
    "Your vision fades.",
    "The cold waters closes over you. Press \\[ENTER]",
    # ENTER does nothing!
    "Is this... the coldness of death?"
]

class Prologue(Screen):
    CSS = """
    #wrapper {
        width: auto;
        height: auto;
        align: center middle;
        layout: vertical;
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
    
    #dialogue {
        margin-bottom: 1;
    }
    
    #hint {
        opacity: 0;
    }
    
    """

    def __init__(self):
        super().__init__()
        self.ENTER = False
        self.SPACE = False
        self.BREAK = False

        # self.dialogue = Label(f"[reverse][b][i]Help me, {username()}[/i][/b][/reverse]\n[dim][i]Save, me.[/i][/]", id="dialogue")
        self.dialogue = Label("", id="dialogue")
        self.hint = Label("[dim]\\[ENTER] to continue[/dim]", id="hint")
        # self.health = Label(" Health: ♥ ♥ ♥ ♡ ♡", id="health")
        # self.stamina = Label("Stamina: ╍╍╍╍╍╍", id="stamina")

    def compose(self) -> ComposeResult:
        with Container(id="wrapper"):
            yield self.dialogue
            yield self.hint
            # with Container(id="sidebar-dock"):
            #     yield self.health
            #     yield self.stamina

    def on_mount(self) -> None:
        self.screen.styles.opacity = 0
        self.call_later(self.sequence)

    @work
    async def sequence(self)-> None:
        self.screen.styles.animate(
            "opacity", value=1.0, duration=1.5,
        )
        await sleep(1.5)
        self.screen.refresh(recompose=True)

        for i in range(len(DIALOGUES)):
            self.hint.styles.opacity = 0
            self.hint.styles.offset = (0, 0)

            await self.typewrite(self.dialogue, DIALOGUES[i])

            await self.hint_animation()

    def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.ENTER = True

    async def wait(self, sec: float = 2, infinite: bool = False) -> None:
        if infinite:
            loops = INFINITE_TIMER
        else:
            loops = int(sec / MICRO_SLEEP)

        for i in range(loops):
            if not self.ENTER:
                await sleep(MICRO_SLEEP)
            else:
                self.ENTER = False
                self.BREAK = True
                break
        self.ENTER = False

    async def typewrite(self, widget: Label, text: str, wait: float = 0.04) -> None:
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
                await sleep(wait)
        widget.update("".join(text))
        self.ENTER = False

    async def hint_animation(self):

        async def hint_wobble(wobble_sec: float = 0.4):
            if not self.BREAK:
                wobble = False
                for _ in range(INFINITE_TIMER):
                    if _ % (wobble_sec / MICRO_SLEEP) == 0:  # 0.4s / 0.01s = 40
                        wobble = not wobble
                        if wobble:
                            self.hint.styles.offset = (1, 0)
                        else:
                            self.hint.styles.offset = (0, 0)

                    if not self.ENTER:
                        await sleep(MICRO_SLEEP)
                    else:
                        self.ENTER = False
                        break
                self.ENTER = False
            self.BREAK = False

        async def hint_fade(time: float = 0.5) -> None:
            self.hint.styles.opacity = 0
            self.hint.styles.animate(
                "opacity",
                value=1.0,
                duration=time
            )
            await sleep(time + 0.1)

        await hint_fade()

        await self.wait(1.5)

        await hint_wobble()

