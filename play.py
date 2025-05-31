import MazeRunner as mr
from tkinter import *
from tkinter.ttk import * 
import random
import time


def left(e):
    print("left")
    game.perform_action(action.LEFT)

def right(e):
    print("right")
    # dx,dy=move_value(1, 0)
    # game.board.move(game.my_player,  game.player_pos[0]+dx, game.player_pos[1]+dy)
    game.perform_action(action.RIGHT)

def up(e):
    print("up")
    # dx,dy=move_value(0, -1)
    # game.board.move(game.my_player,  game.player_pos[0]+dx, game.player_pos[1]+dy)
    game.perform_action( action.UP)
    
def down(e):
    print("down")
    # dx,dy=move_value(0, 1)
    # game.board.move(game.my_player,  game.player_pos[0]+dx, game.player_pos[1]+dy)
    game.perform_action(action.DOWN)

   
  
width=80
r=c=5
master = Tk()
action=mr.RobotAction
game = mr.MazeRunner(master,width,r,c)
game.reset(123)
game.render_game()

master.bind("<Left>",left)
master.bind("<Right>",right)
master.bind("<Down>",down)
master.bind("<Up>",up)
game.start_game()
