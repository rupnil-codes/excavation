from textual.app import App
from textual import events
from assets.save_manager import has_save_file
from screens.intro_screen import IntroScreen
from screens.title_screen import TitleScreen


class UndertaleTUI(App): #our main app class
    
    CSS = """          # again asked gemini but this time it was very simple
    Screen {
        background: #000000;
    }
    """
    
    # Key Binding
    BINGINGS = [("q", "quit", "Quit Game")]
    
    def on_mount(self) -> None:
        if has_save_file():
            self.push_screen(TitleScreen())
        else:
            self.push_screen(IntroScreen())
        
if __name__ == "__main__":
    app = UndertaleTUI()
    app.run()
    
def on_key(self, event: events.Key) -> None:
    if event.key == "escape":
        self.app.exit() # close on esc