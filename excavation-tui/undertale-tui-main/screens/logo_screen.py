from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
import asyncio
from assets.logo import GAME_LOGO
from screens.name_screen import NameScreen
from assets.music_manager import play_sfx_ovr

class LogoScreen(Screen):
# css = gemini

    CSS = """
    LogoScreen {
        align: center middle;
        background: black;
    }
    #logo {
        width: auto;
        height: auto;
        color: white; 
        text-align: center;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("", id="logo")

    def on_mount(self) -> None:
        self.run_worker(self.show_logo())
        play_sfx_ovr("noise")

    async def show_logo(self):
        logo_widget = self.query_one("#logo")
        await asyncio.sleep(1)
        logo_widget.update(GAME_LOGO)
        await asyncio.sleep(3)
        self.app.push_screen(NameScreen())