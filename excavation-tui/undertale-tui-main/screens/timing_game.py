from textual.screen import ModalScreen
from textual.widgets import Label
from textual.containers import Container
from textual.app import ComposeResult
# this file is fixd and moded by gemini
class TimingGame(ModalScreen):
    CSS = """
    TimingGame {
        align: center middle;
        background: 0%; 
    }
    #game-container {
        width: 60;
        height: 5;
        border: solid white;
        background: black;
        align: center middle;
    }
    #bar-label {
        width: 100%;
        text-align: center;
        color: white;
        # No bold here so the blocks render cleanly
    }
    """

    def __init__(self, player_at, is_defense, player_hp_pct, monster_hp_pct):
        super().__init__()
        self.player_at = player_at
        self.is_defense = is_defense
        
        # physics. (not to be that yt shorts guy)
        # 1. CALCULATE SPEED BASED ON HP
        if is_defense:
            # Monster High HP = Fast (Energetic), Low HP = Slow (Tired)
            self.speed = 1.0 + (monster_hp_pct * 2.5)
        else:
            # Player High HP = Slow (Calm), Low HP = Fast (Adrenaline)
            self.speed = 1.0 + ((1.0 - player_hp_pct) * 2.0)

        #calcu zone size
        #green
        green_ticks = 0.3 / 0.05
        green_total_width = self.speed * green_ticks
        self.green_radius = max(1, int(green_total_width / 2))

        #ylw
        yellow_ticks = 0.6 / 0.05
        yellow_total_width = self.speed * yellow_ticks
        self.yellow_radius = max(2, int(yellow_total_width / 2))

        self.width = 50   
        self.position = 0 
        self.direction = 1 
        self.timer = None

    def compose(self) -> ComposeResult:
        with Container(id="game-container"):
            yield Label("", id="bar-label")

    def on_mount(self):
        self.timer = self.set_interval(0.05, self.game_loop)

    def game_loop(self):
        # phy upd
        self.position += (self.speed * self.direction)
        
        # hit edge no bounce modified code
        if self.position >= self.width:
            self.timer.stop()
            fail_result = 1.0 if self.is_defense else 0
            self.dismiss(fail_result)
            return

        # render bloxx
        bar_visual = []
        center = self.width // 2
        
        for i in range(self.width + 1):
            dist = abs(i - center)
            
            # zonedefine
            if dist <= self.green_radius:
                color = "green"    # sweet! (candy crush reference)
            elif dist <= self.yellow_radius:
                color = "yellow"   # ok?
            else:
                color = "red"      # ur trucked
            
            # --- DRAW CHARACTERS ---
            if int(self.position) == i:
                # moving slider on blk backg
                segment = f"[b white on black]║[/]"
            else:
                # solid block
                segment = f"[{color}]█[/]" 
            
            bar_visual.append(segment)

        # scr upd
        self.query_one("#bar-label").update("".join(bar_visual))

    def on_key(self, event):
        if event.key == "enter":
            self.timer.stop()
            self.calculate_result()

    def calculate_result(self):
        center = self.width // 2
        dist = abs(self.position - center)
        
        # logic zonez
        if dist <= self.green_radius:
            # green/perfct
            multiplier = 2.2 if not self.is_defense else 0.0
            
        elif dist <= self.yellow_radius:
            # ylw/ok
            multiplier = 1.0 if not self.is_defense else 0.5
            
        else:
            # red/fail (Weak hit or heavy damage taken)
            multiplier = 0.5 if not self.is_defense else 0.8

        # Send result back
        if not self.is_defense:
            final_damage = int(self.player_at * multiplier)
            self.dismiss(final_damage)
        else:
            self.dismiss(multiplier)

# EVERYTHING AT THE BOTTOM IS COLOUR CIRCLE VERSION, THE ABOVE IS MOVING BAR VERSION
# from textual.screen import ModalScreen
# from textual.widgets import Label
# from textual.containers import Container
# from textual.app import ComposeResult
# import time

# class TimingGame(ModalScreen):
#     # multiplier return based on color
#     # red : 0.2 (Low Dmg) / 1.0 (Full Hit)
#     # ylw : 1.0 (mid dmg) / 0.5 (glancing)
#     # grn : 2.0 (high dmg) / 1.0 (blocked - no dmg)
    
#     # i think ou know by now
#     CSS = """
#     TimingGame { align: center middle; background: 0%; }
#     #game-container { width: 60; height: 5; border: solid white; background: black; align: center middle; }
#     #bar { width: 100%; height: 100%; text-align: center; content-align: center middle; text-style: bold; color: black; }
    
#     /* Dynamic Colors */
#     .red { background: #ff0000; }
#     .yellow { background: #ffff00; }
#     .green { background: #00ff00; }
#     """
    
#     def __init__(self, sped_mult = 1.0, is_defense=False):
#         super().__init__()
#         self.speed = sped_mult
#         self.is_defense= is_defense
#         self.time_elapsed = 0.0
#         self.timer = None
        
#         # cycle r>y>g>y>r
#         self.cycle = [
#             ("red",0.9), 
#             ("yellow", 0.5), 
#             ("green", 0.28),
#             ("yellow", 0.5), 
#             ("red", 0.9)
#         ]
#     def compose(self) -> ComposeResult:
#         with Container(id="game-container"):
#             msg = "PRESS ENTER TO DEFEND!" if self.is_defense else "PRESS ENTER TO ATTACK!"
#             yield Label(msg, id="bar")
            
#     def on_mount(self):
#         # gemini said to add 0.05s / 20fps -- idk bro
#         self.timer = self.set_interval(0.05, self.game_loop)
#     def game_loop(self):
#         self.time_elapsed += 0.05 * self.speed
        
#         current_time = 0
#         phase_color = "red" #initially
        
#         for color, duration in self.cycle:
#             if self.time_elapsed < (current_time + duration):
#                 phase_color = color
#                 break
#             current_time += duration
#         else:
#             # Time ran out!
#             self.dismiss(0.0 if not self.is_defense else 1.0) #hit or miss lol
#             return

#         bar = self.query_one("#bar")
#         bar.remove_class("red", "yellow", "green")
#         bar.add_class(phase_color)
#     def on_key(self, event):
#         if event.key == "enter":
#             self.timer.stop()
#             bar = self.query_one("#bar")
#             # calc multiplyr
#             if "green" in bar.classes:
#                 mult = 0.0 if self.is_defense else 2.0
#             elif "yellow" in bar.classes:
#                 mult = 0.5 if self.is_defense else 1.0
#             else: # if red
#                 mult = 1.0 if self.is_defense else 0.2
                
#             self.dismiss(mult)