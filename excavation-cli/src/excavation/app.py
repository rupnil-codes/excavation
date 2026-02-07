# TEST MAIN MENU
from time import sleep
import os
import keyboard

choice = 0

lis =[
    "Start",
    "Continue",
    "Quit"
]

def clear() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

while True:
    for i in range(len(lis)):
        if choice == i:
            print("-> "+lis[i])
        else:
            print(lis[i])
    sleep(0.2)
    keypress = keyboard.read_key()
    if keypress == "down" and choice != 2:
        choice += 1
    elif keypress == "up" and choice != 0:
        choice -= 1
    clear()