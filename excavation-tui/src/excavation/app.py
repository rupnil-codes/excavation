from textual.app import App
from textual import events
from scenes.MainMenu import MainMenu

class Excavation(App):
    CSS_PATH = "scenes\\css\\excavation.tcss"

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.exit()  # close on esc

    def on_mount(self) -> None:
        self.push_screen(MainMenu())

if __name__ == "__main__":

    app = Excavation()
    app.run()

# Textual Python Code Reload: https://blog.pecar.me/textual-code-reload