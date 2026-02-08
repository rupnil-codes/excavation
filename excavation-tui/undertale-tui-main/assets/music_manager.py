#commented almost everything lmao
import os
#hide hello world from pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

#initialize
try:
    pygame.mixer.init()
except Exception as e:
    print(f"{e}: Pygame audio could not be played, please try using the pygame-ce release or there could be something wrong with the code.")

#assign music dir
MUSIC_DIR = "assets/music"
# map names with real names
TRACK_LIST = {
    "intro": "mus_story.ogg",
    "menu": "mus_menu0.ogg",
    "ruins": "mus_ruins.ogg",
    "battle": "mus_battle1.ogg",
    "death": "mus_gameover.ogg",
    "shop": "mus_shop.ogg",
    "noise": "mus_intronoise.ogg",
    "creation": "mus_menu1.ogg",
    "voice": "mus_sfx_a_grab.ogg"
}
current_track = None

def play_music (track_name):
    global current_track
    # neverb restart the song
    if current_track == track_name:
        return
    # check if track exists
    if track_name not in TRACK_LIST:
        print(f"Track '{track_name}' not defined!")
        return
    
    filename = TRACK_LIST[track_name]
    path = os.path.join(MUSIC_DIR, filename)
    
    #check if musicfile exists
    if not os.path.exists(path):
        print(f"Music file fissing; {filename}")
        return
    try:
        #fade out old muzik/sfx
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1) #-1 means loop
        current_track = track_name
    except Exception as e:
        print(f"Couldn't play music: {e}")
def stop_music():
    global current_track
    pygame.mixer.music.fadeout(1000)
    current_track = None
    
def play_sfx_ovr (track_name):
    global current_track
    # check if track exists
    if track_name not in TRACK_LIST:
        print(f"Track '{track_name}' not defined!")
        return
    
    filename = TRACK_LIST[track_name]
    path = os.path.join(MUSIC_DIR, filename)
    
    #check if sfx file exists
    if not os.path.exists(path):
        print(f"sfx file fissing; {filename}")
        return
    try:
        #fade out old muzik/sfx
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play() #no loop
        current_track = track_name
    except Exception as e:
        print(f"Couldn't play sfx: {e}")
        
def play_sfx(track_name):
    
    if track_name not in TRACK_LIST:
        print(f"SFX '{track_name}' not defined!")
        return
    
    filename = TRACK_LIST[track_name]
    path = os.path.join(MUSIC_DIR, filename)
    
    if not os.path.exists(path):
        print(f"SFX file missing: {filename}")
        return

    try:
        
        effect = pygame.mixer.Sound(path)
        
        effect.play() 
        
    except Exception as e:
        print(f"Couldn't play SFX: {e}")