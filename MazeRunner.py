# Imports each and every method and class of module tkinter and tkinter.ttk
from enum import Enum
import random
from tkinter import *
from tkinter.ttk import * 
import numpy as np
from PIL import Image, ImageTk
from os import path

# Actions the Robot is capable of performing i.e. go in a certain direction
class RobotAction(Enum):
    LEFT=0
    DOWN=1
    RIGHT=2
    UP=3
    
# class of the game the Robot is capable of performing
class MazeRunner:
    
    def __init__(self,master,width=100, row=4, column=4, fps=1):
        
        # Sets the geometry and position of window on the screen
        self.WIDTH=width
        self.Row=row
        self.Column=column
        self.fps = fps
        
        # init remaining variables
        self.restart = False 
        
        # Sets the title to Shapes
        self.master = master
        self.master.title("MazrRunner")
        
        #Load an image in the script
        file_name1 = path.join(path.dirname(__file__), "sprites/bot_blue.png")
        file_name2 = path.join(path.dirname(__file__), "sprites/diamond.png")
        
        self.img_bot= ImageTk.PhotoImage(Image.open(file_name1))
        
        self.img_diamond= ImageTk.PhotoImage(Image.open(file_name2))
        
        # Draw grid
        self.board = Canvas(self.master, width=self.Row*self.WIDTH, height=self.Column*self.WIDTH)
        
        
        self.board.pack()
        
    #######################
    # Initialize game
    def reset(self, seed=None):
        # Random Target position
        self.seed=seed
        random.seed(seed)
        
        self.my_player=0 
        self.score = 1
        self.restart = False
        
        # Initialize object places, player and reward position
        
        self.player_pos=self.gen_player_pos()
        self.reward_pos=self.gen_reward_pos()
        self.OBJECTS_Points=self.init_boards()
        
    
                   
    #######################
    # initialize blocks in board
    def init_boards(self):
       
        OBJECTS=[]
        # n_Blocks=2
        # points=[]
        # points.append(self.player_pos)
        # points.append(self.reward_pos)
        # for i in range(n_Blocks):
        #     while True:
        #         x=random.randint(0,self.Row-1)
        #         y=random.randint(0,self.Column-1)
        #         check=self.check_point_list([x,y],points)    
        #         if check:
        #             points.append([x,y])
        #             OBJECTS.append([x,y])
        #             break
        
        x=1
        y=1
        OBJECTS.append([x,y])
        x=2
        y=1
        OBJECTS.append([x,y])
        x=2
        y=2
        OBJECTS.append([x,y])
            
        
        return OBJECTS
    #######################
    # initialize player position in board
    def gen_player_pos(self):
        x = random.randint(0, self.Row-1)
        y = 0    
        return [x, y]
    #######################
    # initialize reward position in board
    def gen_reward_pos(self):
        x = random.randint(0, self.Row-1)
        y =  self.Column-1
        return [x, y]
    #######################
    # check generated point in a given list of points
    def check_point_list(self,point,list):
        check_for_rows = [e for e in list if point[0] == e[0] and point[1]== e[1]]

        if check_for_rows==[]:
            return 1
        else:
            return 0  
    #######################
    # Render board game and print game
    def render_game(self):
        
        #Load an image in the script
    
        
        for i in range(self.Row):
            for j in range(self.Column):
                check=self.check_point_list([i,j],self.OBJECTS_Points)    
                if check:
                    color="white"
                else:
                    color="blue"
                    
                self.board.create_rectangle(i*self.WIDTH, j*self.WIDTH,(i+1)*self.WIDTH, (j+1)*self.WIDTH, outline = "black", fill = color, width = 2)
      
        
        #Add image to the Canvas Items
        self.my_player=self.board.create_image(self.player_pos[0]*self.WIDTH,self.player_pos[1]*self.WIDTH,image=self.img_bot,anchor=NW)
        self.board.create_image(self.reward_pos[0]*self.WIDTH,self.reward_pos[1]*self.WIDTH,image=self.img_diamond,anchor=NW)
        
        ##
        # self.board.create_oval(self.reward_pos[0]*self.WIDTH,self.reward_pos[1]*self.WIDTH,(self.reward_pos[0]+1)*self.WIDTH,(self.reward_pos[1]+1)*self.WIDTH,outline = "red", fill = "yellow", width = 2 )
        # self.my_player=self.board.create_oval(self.player_pos[0]*self.WIDTH,self.player_pos[1]*self.WIDTH,(self.player_pos[0]+1)*self.WIDTH,(self.player_pos[1]+1)*self.WIDTH,outline = "red", fill = "green", width = 2 )
        
        
        # Pack the canvas to the main window and make it expandable
        self.board.pack()
    
    #######################
    # Infinite loop breaks only by interrupt                                 
    def start_game(self):
        self.board.mainloop()

    #######################
    # stop and close game
    def stop_game(self):
        return self.board.quit()

    #######################
    # Robot moves to certian position
    def perform_action(self, action):
        
        if self.restart:
            self.reset()
            self.render_game()
        
        # Move Robot to the next cell
        dx=dy=0
        if action==RobotAction.LEFT:
                dx=-1
        elif action==RobotAction.RIGHT:
                dx=1
        elif action==RobotAction.UP:
                dy=-1
        elif action==RobotAction.DOWN:
                dy=1
                
        new_x=self.player_pos[0]+dx
        new_y=self.player_pos[1]+dy
        
        # Check the Robot move not to get out boundaries       
        if (new_x >= 0) and (new_x < self.Row) and (new_y >= 0) and (new_y < self.Column) and not ((new_x, new_y) in self.OBJECTS_Points):
            # move robot
            # if no render then don't move image
            if self.my_player>0:
                self.board.move(self.my_player,  
                            self.player_pos[0]+dx*self.WIDTH, 
                            self.player_pos[1]+dy*self.WIDTH)
            
            # save new position of robot
            self.player_pos = [new_x, new_y]
            
            
        # check if robot hit blocks and return flase
        # target_reached False
        for [i, j] in self.OBJECTS_Points:
            if new_x == i and new_y == j:
                print("Fail! score: ")
                self.restart = True
                return False
            
        # check if robot hit reward and return true
        # target_reached True
        if new_x == self.reward_pos[0] and new_y == self.reward_pos[1]:
            print("Success! score: ")
            self.restart = True
            return True
        
    #######################
    # # restart game if robot hit block    
    # def restart_game(self,seed=None):
        
    #     self.score = 1
    #     self.restart = False
    #     # Initialize object places, player and reward position
    #     #self.OBJECTS_Points=self.init_boards()
    #     # Random Target position
    #     self.seed=seed
    #     random.seed(seed)
    #     # self.player_pos=self.player_pos_temp
    #     self.render_game()
        