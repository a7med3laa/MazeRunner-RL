import threading
import MazeRunner as mz
from tkinter import *
from tkinter.ttk import * 
import random
import time


def start():
    while True:
        time.sleep(1)
        action=random.randint(0,3)
        move_action=mz.RobotAction(action)
        print(move_action)
        x=game.perform_action(move_action)
        print(x)
        time.sleep(0.03)


width=80
r=c=4

master = Tk()

game = mz.MazeRunner(master,width,r,c)
game.reset()
game.render_game()

# Start game
t = threading.Thread(target=start)
t.daemon = True
t.start()


game.start_game()
    