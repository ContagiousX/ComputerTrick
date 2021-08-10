import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pyautogui
import math


delay = 0.001
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                # Radius 
                R = 400
                # measuring screen size
                (x,y) = pyautogui.size()
                # locating center of the screen 
                (X,Y) = pyautogui.position(x/2,y/2)
                # offsetting by radius 
                pyautogui.moveTo(X+R,Y)

                for i in range(360):
                    # setting pace with a modulus 
                    if i%6==0:
                        pyautogui.moveTo(X+R*math.cos(math.radians(i)),Y+R*math.sin(math.radians(i)))
                time.sleep(self.delay)
            time.sleep(0.1)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()