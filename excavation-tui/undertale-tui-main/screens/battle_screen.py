from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container
from textual import on
import textwrap
import random
from assets.music_manager import play_music

# file imports
from screens.act_menu import ActMenu
from screens.item_menu import ItemMenu
from screens.mercy_menu import MercyMenu
from screens.timing_game import TimingGame
from screens.victory_screen import VictoryScreen
from assets.player_stats import player, gain_exp, gain_gold
from assets.monsters_data import MONSTER_LIST
from assets.sprites import MONSTER_SPRITES

class BattleScreen(Screen):
    BINDINGS = [
        ("right", "app.focus_next", "Next"),
        ("left", "app.focus_previous", "Previous"),
    ]
    # gemini = css = gemini = css = gemini
    CSS = """
    BattleScreen { layout: vertical; align: center middle; background: black; color: white; }
    #monster-area {
        height: 15; width: 100%; content-align: center middle; text-align: center; text-style: bold; color: white;
    }
    #middle-container { width: 100%; height: auto; align: center middle; }
    #dialogue-box { height: 8; width: 60; border: solid white; padding: 1 2; margin-bottom: 1; text-align: left; }
    #status-bar { height: 3; width: 60; content-align: center middle; color: white; text-style: bold; }
    #button-row { height: 5; width: 100%; align: center middle; layout: horizontal; margin-top: 1; }
    Button { width: 1fr; margin: 0 1; background: #000000; color: #ff9900; border: solid #ff9900; text-style: bold; }
    Button:focus, Button:hover { background: #ff9900; color: #000000; border: solid yellow; text-style: bold; }
    """
    
    def __init__(self):
        super().__init__()
        # load stats
        self.player_name = player["name"]
        self.player_hp = player["hp"]
        self.player_max_hp = player["max_hp"]
        
    def compose(self) -> ComposeResult:
        yield Static("...", id="monster-area")
        with Container(id="middle-container"):
            yield Static("* You encountered a Monster!", id="dialogue-box")
            status_text = f"{self.player_name}   LV {player['lv']}   [yellow]HP[/yellow] {self.player_hp}/{self.player_max_hp}"
            yield Static(status_text, id="status-bar")
        with Container(id="button-row"):
            yield Button("FIGHT", id="btn-fight")
            yield Button("ACT", id="btn-act")
            yield Button("ITEM", id="btn-item")
            yield Button("MERCY", id="btn-mercy")

    def on_mount(self):
        self.load_random_monster()
        play_music("battle")

    #player turn
    def start_player_turn(self):
        # unlock buttons
        self.query("Button").set(disabled=False)
        self.query_one("#btn-fight").focus()
        
        #random flavour text
        flavor_list = self.current_monster.get("random_texts", [])
        
        if flavor_list:
            #pick random line
            text = random.choice(flavor_list)
            self.query_one("#dialogue-box").update(f"* {text}")
        else:
            #fallback text
            self.query_one("#dialogue-box").update(f"* {self.current_monster['name']} is waiting.")
            
    def load_random_monster(self):
        data = random.choice(MONSTER_LIST)
        self.current_monster = data.copy()
        
        self.current_monster["max_hp"] = data["hp"]
        
        self.update_monster_visuals()
        
        box = self.query_one("#dialogue-box")
        box.update(f"* {data['name']} blocks the way!")
    def update_monster_visuals(self):
        # health bar (added new!)
        if not self.current_monster: return
        curr = self.current_monster["hp"]
        maximum = self.current_monster["max_hp"]
        # prevent - vqals
        curr = max(0, curr)
        
        bar_width = 20 # 20 char bar
        if maximum > 0:
            percent = curr / maximum
        else:
            percent = 0
            
        filled = int(bar_width * percent)
        empty = bar_width - filled
        
        # dynamic clolur
        health_bar = f"[green]{'=' * filled}[/green][red]{'-' * empty}[/red]"
        
        # get sprite
        name_key = self.current_monster['name'].lower()
        raw_art = MONSTER_SPRITES.get(name_key, MONSTER_SPRITES["default"])
        sprite_art = textwrap.dedent(raw_art).strip()
        
        # scr upd
        full_display = f"{health_bar}\n\n[green]{sprite_art}[/green]\n\n[ {self.current_monster['name']} ]"
        
        self.query_one("#monster-area").update(full_display)

    def enemy_turn(self):
        box = self.query_one("#dialogue-box")
        
        # after minigame
        def handle_defense(damage_mult):
            #stat get
            monster_atk = self.current_monster["atk"]
            player_def = player["def"]
            
            #calc base dmg
            # base_damage = max(1, monster_atk - (player_def // 5)) 
            raw_damage = max(1, monster_atk - (player_def // 4))
            
            #apply blok mult
            final_damage = int(raw_damage * damage_mult)
            
            # hp upd
            self.player_hp -= final_damage
            if self.player_hp < 0: self.player_hp = 0
            
            # visual upd
            self.query_one("#status-bar").update(
                f"{self.player_name}   LV {player['lv']}   [yellow]HP[/yellow] {self.player_hp}/{self.player_max_hp}"
            )
            
            if final_damage == 0:
                msg = f"* Blocked! You took 0 damage."
            else:
                msg = f"* You took {final_damage} damage!"
            box.update(msg)

            # check if died
            if self.player_hp <= 0:
                from screens.game_over import GameOver
                
                def on_game_over(retry):
                    if retry:
                        self.player_hp = self.player_max_hp
                        
                        self.current_monster["hp"] = self.current_monster["max_hp"]
                        self.update_monster_visuals()
                        self.query_one("#status-bar").update(
                            f"{self.player_name}   LV {player['lv']}   [yellow]HP[/yellow] {self.player_hp}/{self.player_max_hp}"
                        )
                        box.update("* But it refused.")
                        self.start_player_turn()
                    else:
                        self.dismiss()

                self.set_timer(1.5, lambda: self.app.push_screen(GameOver(), on_game_over))
            else:
                self.set_timer(1.5, self.start_player_turn)

        #calc hp perc
        p_pct = self.player_hp / self.player_max_hp
        m_pct = 0
        if self.current_monster["max_hp"] > 0:
            m_pct = self.current_monster["hp"] / self.current_monster["max_hp"]

        # def start
        self.app.push_screen(
            TimingGame(player_at=0, is_defense=True, player_hp_pct=p_pct, monster_hp_pct=m_pct), 
            handle_defense
        )

    @on(Button.Pressed)
    def handle_buttons(self, event: Button.Pressed):
        btn_id = event.button.id
        box = self.query_one("#dialogue-box")

        if btn_id == "btn-fight": #rev 2
            #disable buttons
            self.query("Button").set(disabled=True)
            
            def handle_damage(damage):
                self.current_monster["hp"] -= damage
                self.update_monster_visuals()
                
                #hit texts
                if damage > player["atk"] * 1.2:
                    msg = f"* CRITICAL HIT! ({damage} dmg)"
                elif damage < player["atk"]:
                    msg = f"* Weak hit... ({damage} dmg)"
                else:
                    msg = f"* You attacked. ({damage} dmg)"
                
                box.update(msg)
                
                #if enemy alive
                if self.current_monster["hp"] > 0:
                    self.set_timer(1.5, self.enemy_turn)
                else:
                    #victory---
                    xp = self.current_monster.get("exp", 0)
                    gold = self.current_monster.get("gold", 0)
                    
                    gain_gold(gold)
                    is_levelup = gain_exp(xp)
                    
                    def on_win(result):
                        self.dismiss()

                    self.set_timer(1.0, lambda: self.app.push_screen(
                        VictoryScreen(xp, gold, leveled_up=is_levelup), 
                        on_win
                    ))

            #calc perc
            p_pct = self.player_hp / self.player_max_hp
            m_pct = 0
            if self.current_monster["max_hp"] > 0:
                m_pct = self.current_monster["hp"] / self.current_monster["max_hp"]

            #launch timing game(most fixes)
            self.app.push_screen(TimingGame(
                player_at=player["atk"],    
                is_defense=False,           
                player_hp_pct=p_pct,        
                monster_hp_pct=m_pct        
            ), handle_damage)
            
        elif btn_id == "btn-act":
            acts = self.current_monster['acts']
            def handle_act(choice):
                if choice is None: return  # ec press
                
                flavor = acts.get(choice, "Nothing happened.")
                
                if choice == "check":
                    stats = f"HP {self.current_monster['hp']}/{self.current_monster['max_hp']} ATK {self.current_monster['atk']} DEF {self.current_monster.get('df', 0)}"
                    box.update(f"* CHECK: {self.current_monster['name']}\n* {stats}\n* {flavor}")
                    
                else:
                    self.query("Button").set(disabled=True)
                    box.update(f"* {choice.replace('_', ' ').capitalize()} \n* {flavor}")
                    self.set_timer(2.0, self.enemy_turn)
            self.app.push_screen(ActMenu(acts), handle_act)

        elif btn_id == "btn-item":
            def handle_item(choice):
                if choice is None: return # esc press
                self.query("Button").set(disabled=True)
                self.player_hp = min(self.player_hp + 10, self.player_max_hp)
                if choice in player["inventory"]: player["inventory"].remove(choice)
                
                self.query_one("#status-bar").update(
                    f"{self.player_name}   LV {player['lv']}   [yellow]HP[/yellow] {self.player_hp}/{self.player_max_hp}"
                )
                box.update(f"* You ate {choice}.\n* Recovered 10 HP!")
                self.set_timer(2.0, self.enemy_turn)

            self.app.push_screen(ItemMenu(player["inventory"]), handle_item)

        elif btn_id == "btn-mercy":
            # ylw if spareable
            current_hp = self.current_monster["hp"]
            max_hp = self.current_monster["max_hp"]
            hp_pct = current_hp / max_hp
            
            can_spare_now = hp_pct <= 0.15

            def handle_mercy(choice):
                if choice is None: return 
                
                self.query("Button").set(disabled=True)

                if choice == "spare":
                    #recheck logic
                    if can_spare_now:
                        box.update(f"* {self.current_monster['name']} was spared.")
                        
                        gold = self.current_monster.get("gold", 0)
                        gain_gold(gold)
                        
                        def on_win(result):
                            self.dismiss()
                        
                        self.set_timer(1.0, lambda: self.app.push_screen(VictoryScreen(0, gold), on_win))
                    else:
                        box.update(f"* Spare failed. {self.current_monster['name']} won't listen yet.")
                        self.set_timer(1.5, self.enemy_turn)

                elif choice == "flee":
                    # 40% success
                    if random.random() < 0.40:
                        box.update("* I'm outta here.....")
                        self.set_timer(1.0, self.dismiss)
                    else: #60% fail
                        box.update("* Escape failed! Don't trip next time..")
                        self.set_timer(1.5, self.enemy_turn)

            self.app.push_screen(MercyMenu(can_spare=can_spare_now), handle_mercy)