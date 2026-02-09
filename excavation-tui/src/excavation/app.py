from textual.app import App
from textual import events

from scenes.main_menu import MainMenu
from scenes.new_game import NewGame
from scenes.splash_screen import SplashScreen

class Excavation(App):
    CSS_PATH = "css\\excavation.tcss"

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.exit()  # close on esc

    def on_mount(self) -> None:
        self.install_screen(MainMenu(), "main_menu")
        self.install_screen(NewGame(), "new_game")
        self.install_screen(SplashScreen(), "splash_screen")

        self.push_screen("main_menu")

if __name__ == "__main__":

    app = Excavation()
    app.run()

# Textual Python Code Reload: https://blog.pecar.me/textual-code-reload