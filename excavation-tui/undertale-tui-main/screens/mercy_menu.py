from textual.screen import ModalScreen
from textual.widgets import ListView, ListItem, Label
from textual.app import ComposeResult
from textual import on

class MercyMenu(ModalScreen):
    BINDINGS = [("escape", "cancel", "Back")]
    # gemini wries csss
    CSS = """
    MercyMenu { align: center middle; background: 0%; }
    #menu-box { width: 60; height: 10; border: solid white; background: black; padding: 1 2; }
    ListItem { color: white; }
    #spare { color: white; } 
    #flee { color: white; }
    ListItem:hover { background: #ff9900; color: black; text-style: bold; }
    """

    def __init__(self, can_spare=False):
        super().__init__()
        self.can_spare = can_spare

    def compose(self) -> ComposeResult:
        if self.can_spare:
            spare_text = "[yellow]* Spare[/yellow]"
        else:
            spare_text = "* Spare"
        
        items = [
            ListItem(Label(spare_text), id="spare"),
            ListItem(Label("* Flee"), id="flee")
        ]
        
        yield ListView(*items, id="menu-box")

    def action_cancel(self):
        self.dismiss(None)

    @on(ListView.Selected)
    def on_select(self, event: ListView.Selected):
        if event.item:
            self.dismiss(event.item.id)