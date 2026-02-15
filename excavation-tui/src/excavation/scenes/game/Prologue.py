from asyncio import sleep

from textual import work, events
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.app import ComposeResult

from widgets import username, play_sound

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
    
    #health {
        text-align: center;
        color: #b23434;
        margin: 1;
    }
    
    #stamina {
        text-align: center;
        color: yellow;
        margin: 1;
    }
    
    #dialogue {
        margin-bottom: 1;
    }
    
    """

    ENTER = False
    SPACE = False
    BREAK = False

    # dialogue = Label(f"[reverse][b][i]Help me, {username()}[/i][/b][/reverse]\n[dim][i]Save, me.[/i][/]", id="dialogue")
    dialogue = Label("", id="dialogue")
    hint = Label("", id="hint")
    health = Label(" Health: ♥ ♥ ♥ ♡ ♡", id="health")
    stamina = Label("Stamina: ╍╍╍╍╍╍", id="stamina")

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

    async def wait(self, sec: float = 2, infinite: bool = False) -> None:
        micro_sleep = 0.01

        if infinite:
            loops = 999999
        else:
            loops = int(sec / micro_sleep)

        for i in range(loops):
            if not self.ENTER:
                await sleep(micro_sleep)
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
                await sleep(0.04)
        widget.update("".join(text))
        self.ENTER = False

    opacity_step = 0
    fade_timer = None

    # async def fade_hint(self):
    #     self.opacity_step = 0
    #     self.hint.styles.opacity = 0
    #     self.fade_timer = self.set_interval(0.05, )
    #     for _ in range(int(2/0.05)):
    #         self.wait(0.05)
    #         self.fade_step()

    # def fade_step(self):
    #     self.opacity_step += 0.05 / 2  # total duration = 2 seconds
    #
    #     if self.ENTER:
    #         self.hint.styles.opacity = 0
    #         self.fade_timer.stop()
    #
    #     if self.opacity_step >= 1:
    #         self.opacity_step = 1
    #         self.fade_timer.stop()
    #
    #     self.hint.styles.opacity = self.opacity_step

    @work
    async def sequence(self)-> None:
        self.hint.styles.opacity = 0
        self.screen.styles.animate(
            "opacity", value=1.0, duration=1.5,
        )
        await sleep(1.5)
        self.screen.refresh(recompose=True)

        for i in range(len(DIALOGUES)):
            await self.typewrite(self.dialogue, DIALOGUES[i])

            self.hint.update("[dim]\\[ENTER] to continue[/dim]")
            self.hint.styles.animate(
                "opacity",
                value=1.0,
                duration=0.4
            )
            await sleep(0.5)

            for _ in range(int(1.5/0.05)):
                if not self.ENTER:
                    await sleep(0.05)
                else:
                    self.ENTER = False
                    self.BREAK = True
                    break
            self.ENTER = False

            if not self.BREAK:
                wobble = False
                for _ in range(999999):
                    if _ % 8 == 0:  # 8 * 0.05s = 0.4s
                        wobble = not wobble
                        if wobble:
                            self.hint.styles.offset = (1, 0)
                        else:
                            self.hint.styles.offset = (0, 0)

                    if not self.ENTER:
                        await sleep(0.05)
                    else:
                        self.ENTER = False
                        break
                self.ENTER = False
            self.BREAK = False

            self.hint.styles.opacity = 0
            self.hint.styles.offset = (0, 0)

    def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.ENTER = True
