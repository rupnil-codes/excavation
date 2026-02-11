import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame

try:
    pygame.init()
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=512
    )
except Exception as e:
    print(e)

_sound_cache = {}

SOUNDS_DIR = os.path.join("assets", "sounds")
SFX_DIR = os.path.join(SOUNDS_DIR, "sfx")
TRACKS_DIR = os.path.join(SOUNDS_DIR, "tracks")

SFX_LIST = {
    "glitch": "glitch.wav",
    "type": "type.wav",
}
TRACKS_LIST = {
    "menu_track": "menu_track.mp3",
}

def play_sound(
        sound: str,
        volume:  float = 1.0,
        loops: bool = False,
        maxtime: int = 0,
        fade_ms: int = 0,
):
    try:
        if sound not in _sound_cache:
            path = os.path.join(SFX_DIR, SFX_LIST[sound])
            _sound_cache[sound] = pygame.mixer.Sound(path)

        sound = _sound_cache[sound]
        sound.set_volume(volume)
        if loops:
            sound.play(
                loops=-1,
                maxtime=maxtime,
                fade_ms=fade_ms,
            )
        else:
            sound.play(
                loops=0,
                maxtime=maxtime,
                fade_ms=fade_ms,
            )
    except Exception as error:
        print(error)


def play_track(
        track: str,
        volume: float = 1.0,
        loops: bool = False,
        start: float = 0.0,
        fade_ms: int = 0,
):
    try:
        path = os.path.join(TRACKS_DIR, TRACKS_LIST[track])
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        if loops:
            pygame.mixer.music.play(
                loops=-1,
                start=start,
                fade_ms=fade_ms,
            )
        else:
            pygame.mixer.music.play(
                loops=0,
                start=start,
                fade_ms=fade_ms,
            )
    except Exception as error:
        print(error)

def stop():
    try:
        pygame.mixer.stop()
    except Exception as er:
        print(er)

def fade_out(sec: int):
    try:
        pygame.mixer.music.fadeout(sec*1000)
        pygame.mixer.music.fadeout(sec*1000)
    except Exception as er:
        print(er)
