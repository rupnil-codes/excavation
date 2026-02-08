from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events
import asyncio
from assets.story_text import INTRO_LINES
from screens.logo_screen import LogoScreen
from assets.save_manager import load_game, has_save_file
from assets.music_manager import play_music

# i took help from gemini for css
class IntroScreen(Screen):
    """The opening cutscene of the game."""

    CSS = """
    IntroScreen {
        align: center middle;
        background: #000000;
        color: #ffffff;
    }
    #story-box {
        width: 80%;
        height: auto;
        border: solid white; 
        padding: 1 2;
        text-align: center;
        text-style: bold;
    }
    """
# that css was complex ig ahh
    def compose(self) -> ComposeResult:
        yield Static("", id="story-box")
    def on_mount(self) -> None:
        self.story_widget = self.query_one("#story-box")
        self.run_worker(self.play_intro())
        play_music("intro")
    async def play_intro(self):
# it will type the story line by line
        await asyncio.sleep(1.0) #pause at start

        for line in INTRO_LINES:
            self.story_widget.update("") 
            
            displayed_text = ""
            for char in line:
                displayed_text += char
                self.story_widget.update(displayed_text)
                await asyncio.sleep(0.05) # i removex complex num
            
            # reading time
            await asyncio.sleep(2.0) 
        
        # Next part------
        self.story_widget.update("[blink]PRESS ENTER TO GET IN[/blink]")
    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.push_screen(LogoScreen()) # skip on enter