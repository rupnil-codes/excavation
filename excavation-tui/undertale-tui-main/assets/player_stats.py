player = { # player varibs
    "name" : "Undertale", # fallback
    "lv" : 1, #lv is 1 initially
    "hp" : 20,
    "max_hp": 20, #incs with lv
    "exp": 0,
    "gold": 0,
    "atk": 10,  #incs w lv           
    "def": 10,  #inx wiht lv          
    "inventory": ["Monster Candy", "Spider Donut"]
}

# lv : xp
LV_THRESHOLDS = {
    2: 10,
    3: 30,
    4: 70,
    5: 120,
    6: 200,
    7: 300,
    8: 500,
    9: 800,
    10: 1200,
    20: 50000
}

def gain_gold(amount):
    # gold add to player state variable
    player["gold"] += amount
def gain_exp(amount):
    player["exp"] += amount
    leveled_up = False
    
    current_lv = player["lv"]
    next_lv = current_lv + 1
    
    # lvl jump (loop if multiple jump)
    while next_lv in LV_THRESHOLDS and player["exp"] >= LV_THRESHOLDS[next_lv]:
        player["lv"] = next_lv
        player["max_hp"] += 4 # hp limit goes up
        player["hp"] = player["max_hp"] # full heal
        player["atk"] += 2 # inc strengh
        player["def"] += 2 # inc def
        leveled_up = True
        next_lv += 1
    return leveled_up