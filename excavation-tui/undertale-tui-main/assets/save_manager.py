import json
import os
from assets.player_stats import player

# save file name
SAVE_FILE = "savegame.json"
def save_game():
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(player, f)
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False
def load_game():
    # check if save file exsis
    if not os.path.exists (SAVE_FILE):
        return False
    try:
        with open (SAVE_FILE, "r") as f:
            data = json.load(f)
        player.update(data)
        return True
    except Exception as e:
        print(f"Error loading: {e}")
        return False
    
def has_save_file():
    return os.path.exists(SAVE_FILE)