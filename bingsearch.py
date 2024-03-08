import pyautogui
import time
import random
import subprocess
from pynput.keyboard import Listener, Key
import threading
import sys

running = True
arr = []
textFilepath = r"searchlist.txt"
EdgeDirectory = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

def on_press(key):
    global running
    if key == Key.esc:
        running = False

def keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def openEdge(dir):
    try:
        subprocess.Popen([dir])
    except Exception as e:
        print(f"Error occurred while opening Edge: {e}")
        sys.exit(1)

def getRandomStr(wordlist):
    return random.choice(wordlist)
    
def webSearch():
    global running
    while running:
        try:
            pyautogui.hotkey('ctrl', 't')
            time.sleep(1)
            string = getRandomStr(arr)
            searched_string = string.strip().replace('"', '').replace(',', "")
            
            for word in searched_string:
                [pyautogui.write(character) for character in word]
                interval = random.uniform(0, .2)
                time.sleep(interval)
                
            pyautogui.press('enter')
            time.sleep(8)
            pyautogui.hotkey('ctrl', 'w')
        except Exception as e:
            print(f"Error occurred during web search: {e}")
            sys.exit(1)

if __name__ == "__main__":
    keyboard_thread = threading.Thread(target=keyboard_listener)
    keyboard_thread.start()
    count = 0
    try:
        with open(textFilepath) as f:
            for line in f:
                arr.append(line.replace("\'", '').replace("\\n", "").replace(" \n", "").replace("', '", ""))
        openEdge(EdgeDirectory)
        time.sleep(2)
        while running:
            webSearch()
            count += 1
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        keyboard_thread.join()
