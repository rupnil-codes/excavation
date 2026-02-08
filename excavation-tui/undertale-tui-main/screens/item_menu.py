# act menu took as base
#code fixed by gemini
from textual.screen import ModalScreen
from textual.widgets import ListView, ListItem, Label
from textual.app import ComposeResult
from textual import on

class ItemMenu(ModalScreen):
    BINDINGS = [("escape", "cancel", "Back")]
#css = yk
    CSS = """ 
    ItemMenu { align: center middle; background: 0%; }
    #menu-box { width: 60; height: 10; border: solid white; background: black; padding: 1 2; }
    ListItem { color: white; }
    ListItem:hover { background: #ff9900; color: black; text-style: bold; }
    """

    def __init__(self, inventory_list):
        super().__init__()
        self.inventory = inventory_list
        self.mapping = {}

    def compose(self) -> ComposeResult:
        items = []
        if not self.inventory:
            items.append(ListItem(Label("* (Empty)"), id="empty"))
        else:
            for index, item_name in enumerate(self.inventory):
                safe_id = f"item-{index}"
                self.mapping[safe_id] = item_name
                items.append(ListItem(Label(f"* {item_name}"), id=safe_id))
        
        yield ListView(*items, id="menu-box")

    def action_cancel(self):
        self.dismiss(None)

    @on(ListView.Selected)
    def on_select(self, event: ListView.Selected):
        if not event.item: return
        
        selected_id = event.item.id
        if selected_id == "empty":
            self.dismiss(None)
        else:
            self.dismiss(self.mapping.get(selected_id))
#  Orig Code
# from textual.screen import ModalScreen
# from textual.widgets import ListView, ListItem, Label
# from textual.app import ComposeResult
# from textual import on

# class ItemMenu(ModalScreen):
#     CSS = """
#     ItemMenu {
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
    
#     ListItem {
#         color: white;
#     }
    
#     ListItem:hover {
#         background: #ff9900;
#         color: black;
#         text-style: bold;
#     }
#     """

#     def __init__(self, inventory_list):
#         super().__init__()
#         self.inventory = inventory_list

#     def compose(self) -> ComposeResult:
#         items = []
#         if not self.inventory:
#             items.append(ListItem(Label("* (Empty)"), id="empty"))
#         else:
#             for item_name in self.inventory:
#                 # for *
#                 display_text = f"* {item_name}" 
#                 items.append(ListItem(Label(display_text), id=item_name))
        
#         yield ListView(*items, id="menu-box")

#     @on(ListView.Selected)
#     def on_select(self, event: ListView.Selected):
#         if event.item and event.item.id != "empty":
#             self.dismiss(event.item.id)
#         else:
#             self.dismiss(None) # close if no item in inv or cancelled
