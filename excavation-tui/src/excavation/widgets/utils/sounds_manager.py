import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame

try:
    pygame.init()
    pygame.mixer.init()
except Exception as e:
    print(e)

SOUNDS_DIR = os.path.join("assets", "sounds")
TRACK_LIST = {
    "type": "type.mp3",
}

def type_sfx():
    try:
        path = os.path.join(SOUNDS_DIR, "type.mp3")
        sound = pygame.mixer.Sound(path)
        sound.set_volume(1)
        sound.play()
    except Exception as er:
        print(er)

def glitch_sfx():
    try:
        path = os.path.join(SOUNDS_DIR, "scary_scifi.wav")
        sound = pygame.mixer.Sound(path)
        sound.set_volume(1)
        sound.play()

    except Exception as er:
        print(er)

def menu():
    try:
        path = os.path.join(SOUNDS_DIR, "menu_track.mp3")
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
    except Exception as er:
        print(er)

def stop():
    try:
        pygame.mixer.stop()
    except Exception as er:
        print(er)

def fade_out(sec: int):
    try:
        pygame.mixer.music.fadeout(sec*1000)
    except Exception as er:
        print(er)
