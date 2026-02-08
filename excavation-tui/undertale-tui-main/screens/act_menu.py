#code fixed by gemimi
from textual.screen import ModalScreen
from textual.widgets import ListView, ListItem, Label
from textual.app import ComposeResult
from textual import on

class ActMenu(ModalScreen):
    BINDINGS = [("escape", "cancel", "Back")]
# dont think need to mention anymore
    CSS = """
    ActMenu { align: center middle; background: 0%; }
    #menu-box { width: 60; height: 10; border: solid white; background: black; padding: 1 2; }
    ListItem { color: white; }
    ListItem:hover { background: #ff9900; color: black; text-style: bold; }
    """

    def __init__(self, acts_dict):
        super().__init__()
        self.acts = acts_dict

    def compose(self) -> ComposeResult:
        items = []
        for act_key in self.acts.keys():
            # FORMATTING LOGIC:
            # 1. Replace underscores with spaces ("pick_on" -> "pick on")
            # 2. Fix "dont" -> "don't"
            display_name = act_key.replace("_", " ")
            if "dont" in display_name:
                display_name = display_name.replace("dont", "don't")
            
            # 3. Capitalize ("don't pick on" -> "Don't pick on")
            display_text = f"* {display_name.capitalize()}"
            
            # We send the original key (e.g., "pick_on") back to BattleScreen
            items.append(ListItem(Label(display_text), id=act_key))
        
        yield ListView(*items, id="menu-box")

    def action_cancel(self):
        self.dismiss(None) # Return None to signal "Go Back"

    @on(ListView.Selected)
    def on_select(self, event: ListView.Selected):
        if event.item:
            self.dismiss(event.item.id)
# orig code
# from textual.screen import ModalScreen
# from textual.widgets import ListView, ListItem, Label
# from textual.app import ComposeResult
# from textual import on

# class ActMenu(ModalScreen):
#     BINDINGS = [("escape", "cancel", "Back")]

#     CSS = """
#     ActMenu {
#         align: center middle;
#         background: 0%; 
#     }
#     #menu-box {
#         width: 60;
#         height: 10;
#         border: solid white;
#         background: black;
#         padding: 1 2;
#     }
#     ListItem { color: white; }
#     ListItem:hover {
#         background: #ff9900;
#         color: black;
#         text-style: bold;
#     }
#     """

#     def __init__(self, acts_dict):
#         super().__init__()
#         self.acts = acts_dict

#     def compose(self) -> ComposeResult:
#         items = []
#         # make item list
#         for act_name in self.acts.keys():
#             display_text = f"* {act_name.capitalize()}"
#             # makeid safe
#             safe_id = act_name.replace(" ", "_").lower()
#             items.append(ListItem(Label(display_text), id=safe_id))
        
#         yield ListView(*items, id="menu-box")

#     def action_cancel(self):
#         self.dismiss(None)

#     @on(ListView.Selected)
#     def on_select(self, event: ListView.Selected):
#         if event.item:
#             #return id
#             self.dismiss(event.item.id)
#         else:
#             self.dismiss(None)
            
