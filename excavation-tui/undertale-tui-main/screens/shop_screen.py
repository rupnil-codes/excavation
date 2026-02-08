from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Container
from textual import on
from assets.player_stats import player
from assets.shop_data import SHOP_ITEMS, SHOP_DESCRIPTIONS
from assets.music_manager import play_music

class ShopScreen(Screen):
    # 1. Navigation Bindings
    BINDINGS = [
        ("escape", "dismiss", "Exit Shop"),
        ("up", "app.focus_previous", "Move Up"),
        ("down", "app.focus_next", "Move Down")
    ]
    
    CSS = """
    ShopScreen { align: center middle; background: black; }
    #shop-box { 
        width: 70; height: 20; 
        border: double yellow; 
        background: black; 
        layout: horizontal; 
    }
    #item-list { width: 50%; height: 100%; border-right: solid white; padding: 1; }
    #info-panel { width: 50%; height: 100%; padding: 1; text-align: center; }
    
    Button { width: 100%; margin-bottom: 1; background: #222; color: white; border: none; }
    
    /* Highlight Style */
    Button:focus { background: yellow; color: black; text-style: bold; }
    
    #desc-box { height: 1fr; border-top: solid white; margin-top: 1; padding-top: 1; color: #aaa; }
    #gold-display { color: yellow; text-style: bold; margin-bottom: 1; }
    #msg-box { color: green; height: 1; }
    """

    def compose(self) -> ComposeResult:
        with Container(id="shop-box"):
            #left side items
            with Container(id="item-list"):
                yield Label("--- SHOP ---", classes="header")
                for item, price in SHOP_ITEMS.items():
                    safe_id = item.replace(" ", "_")
                    yield Button(f"{item:<15} {price:>4}G", id=safe_id)
            
            #right side info
            with Container(id="info-panel"):
                yield Label(f"GOLD: {player['gold']}", id="gold-display")
                yield Label("", id="msg-box")
                yield Label("Select an item...", id="desc-box")
                yield Button("EXIT", id="btn-exit")

    def on_descendant_focus(self, event):
        widget = event.widget
        if isinstance(widget, Button):
            btn_id = widget.id
            if btn_id == "btn-exit":
                self.query_one("#desc-box").update("Leave the shop.")
                return
            
            if btn_id:
                item_name = btn_id.replace("_", " ")
                if item_name in SHOP_DESCRIPTIONS:
                    self.query_one("#desc-box").update(SHOP_DESCRIPTIONS[item_name])

    #buy
    @on(Button.Pressed)
    def handle_shop(self, event: Button.Pressed):
        btn_id = event.button.id
        
        if btn_id == "btn-exit":
            self.dismiss()
            return

        item_name = btn_id.replace("_", " ")
        
        if item_name in SHOP_ITEMS:
            price = SHOP_ITEMS[item_name]
            
            if player["gold"] >= price:
                player["gold"] -= price
                player["inventory"].append(item_name)
                self.query_one("#gold-display").update(f"GOLD: {player['gold']}")
                self.query_one("#msg-box").update(f"[green]Bought {item_name}![/green]")
            else: #if plyr broke
                self.query_one("#msg-box").update("[red]Not enough G![/red]")
    def on_mount(self):
        play_music("shop")