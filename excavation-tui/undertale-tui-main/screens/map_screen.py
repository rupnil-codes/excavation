from textual.screen import Screen
from textual.widgets import Label, Static
from textual.app import ComposeResult
from textual.events import Key
from textual.containers import Container
import random
import time
from screens.menu_screen import MenuScreen
from screens.shop_screen import ShopScreen
from assets.music_manager import play_music
from widgets.dialogue_box import DialogueBox

#btlscr import
from screens.battle_screen import BattleScreen

class MapScreen(Screen): #css = geminiiiiii
    CSS = """
    MapScreen {
        /* 🚨 CRITICAL: This tells the screen it has two levels */
        layers: base overlay;
        align: center middle;
        background: black;
    }

    #map-container {
        /* 🚨 CRITICAL: Puts the map on the bottom level */
        layer: base;
        
        /* Your styling */
        width: auto;
        height: auto;
        border: solid white;
        background: #000000;
        color: white;
        text-align: center;
    }
    """
    # by gemini
    # 1 = Wall, 0 = Walkable
    # A simple "Ruins" layout
    WORLD_MAP = [
        "########################################",
        "#......................................#",
        "#..##################################..#",
        "#..#................................#..#",
        "#..#..#######..###################..#..#",
        "#..#..#.....#..#.................#..#..#",
        "#..#..#.....#..#.................#..#..#",
        "#..#..#.....#..#.................#..#..#",
        "#..####.....####.................#..#..#",
        "#...................................#..#",
        "#..##################################..#",
        "#......................................#",
        "########################################"
    ]

    def __init__(self):
        super().__init__()
        self.player_x = 2
        self.player_y = 1
        self.steps_taken = 0
        self.frozen = False #new
        self.safe_until = 0 # new 2

    def compose(self) -> ComposeResult:
        with Container(id="map-container"):
            yield Label("", id="map-label")

    def on_mount(self):
        self.render_map()
        self.query_one("#map-label").focus()
        play_music("ruins")
    def on_screen_resume(self):
        play_music("ruins")

    def render_map(self):
        # copy map to draw plyr
        display_map = []
        
        for y, row in enumerate(self.WORLD_MAP):
            if y == self.player_y:
                
                row_chars = list(row)
                row_chars[self.player_x] = "[cyan]@[/cyan]"
                display_map.append("".join(row_chars))
            else:
                display_map.append(row)
        
        # Join rows with newlines
        full_text = "\n".join(display_map)
        self.query_one("#map-label").update(full_text)

    def on_key(self, event: Key):
        if self.frozen:
            return
        if event.key == "c":
            self.app.push_screen(MenuScreen())
            return #added menuscreen 
        if event.key == "s":
            self.app.push_screen(ShopScreen())
            return #added shop
        if event.key == "t":
            # Only open if one isn't already open
            if not self.query("DialogueBox"):
                box = DialogueBox("* Greetings, human.\n* I am a text box.")
                box.styles.layer = "overlay"
                self.mount(box)
        if self.query("DialogueBox"): 
            return
        # calc pos
        target_x = self.player_x
        target_y = self.player_y

        if event.key == "up":
            target_y -= 1
        elif event.key == "down":
            target_y += 1
        elif event.key == "left":
            target_x -= 1
        elif event.key == "right":
            target_x += 1
        else:
            return

        # wall detection
        if 0 <= target_y < len(self.WORLD_MAP) and 0 <= target_x < len(self.WORLD_MAP[0]):
            # check
            tile = self.WORLD_MAP[target_y][target_x]
            if tile != "#":
                #allow movin
                self.player_x = target_x
                self.player_y = target_y
                self.steps_taken += 1
                self.check_encounter()
                self.render_map()
    def check_encounter(self):
        if time.time() < self.safe_until: # add safe for 2 min logic
            return
        #if monsterr!
        if random.random() < 0.05: 
            #freeze
            self.frozen = True
            
            #vusal
            self.query_one("#map-container").border_title = "[red]! ENCOUNTER ![/red]"
            
            def start_battle():
                def on_return(result):
                    self.frozen = False 
                    self.query_one("#map-container").border_title = "" 
                    self.query_one("#map-label").focus() 
                    wait_time = random.randint(60, 120)
                    self.safe_until = time.time() + wait_time # restart timer
                
                self.app.push_screen(BattleScreen(), on_return)

            self.set_timer(1.5, start_battle)