from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Label
from scenes.MainMenu import MainMenu

class Excavation(App[None]):
    CSS_PATH = "scenes\\css\\excavation.css"

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.exit()  # close on esc

    def on_mount(self) -> None:
        self.push_screen(MainMenu())


if __name__ == "__main__":

    app = Excavation()
    app.run()

# Textual Python Code Reload: https://blog.pecar.me/textual-code-reload