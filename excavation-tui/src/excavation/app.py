from textual.app import App
from textual import events

from scenes import (
    MainMenu,
    SplashScreen,
    NewGame,
    Prologue,
)

import os

class Excavation(App):
    CSS = """
Screen {
    align: center middle;
    background: #0d0d0d;
    border: heavy white;
    /*padding: 3 0 0 10;*/
    /*border-top: solid blue;*/
    /*hatch: cross green;*/
}

#wrapper {
    width: auto;
    height: auto;
    align: center middle;
}

#logo{
    margin: 0 0 1 0;
    width: 57;
    height: 6;
    min-width: 57;
    min-height: 7;
    /*margin: 1 0 0 5;*/
}
    """

    # CSS_PATH = os.path.join("css", "excavation.tcss")

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.exit()  # close on esc

    def on_mount(self) -> None:
        self.install_screen(MainMenu(), "main_menu")
        self.install_screen(NewGame(), "new_game")
        self.install_screen(SplashScreen(), "splash_screen")
        self.install_screen(Prologue(), "prologue")

        self.push_screen("prologue")

if __name__ == "__main__":

    app = Excavation()
    app.run()

# Textual Python Code Reload: https://blog.pecar.me/textual-code-reload