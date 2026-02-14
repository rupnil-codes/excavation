import random

GLITCH_CHARS = list("█▓▒░@#$%&?|<>[]{}")

def glitch_text(text: str, intensity: float = 0.35) -> str:
    glitched = ""
    forbidden_chars = [" ", "[", "]", "/", "\\"]
    for char in text:
        if char not in forbidden_chars and random.random() < intensity:
            glitched += random.choice(GLITCH_CHARS)
        else:
            glitched += char

    return glitched