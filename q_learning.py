'''
Example of using Q-Learning to train our custom environment.
'''
import threading
import time
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
import os
import MaveRunner_Gymnisuim_Env # Even though we don't use this class here, we should include it here so that it registers the WarehouseRobot environment.

# Train or test using Q-Learning
def train_q_learning(episodes, render=False):

    env = gym.make('maze-runner-v0', render_mode='human' if render else None)

    
    # initialize the Q Table, a 5D vector: [robot_row_pos, robot_row_col, target_row_pos, target_col_pos, actions]
    q = np.zeros((env.unwrapped.grid_rows, env.unwrapped.grid_cols, env.unwrapped.grid_rows, env.unwrapped.grid_cols, env.action_space.n))
    
    
    # Hyperparameters
    learning_rate_a = 0.9   # alpha or learning rate
    discount_factor_g = 0.9 # gamma or discount rate. Near 0: more weight/reward placed on immediate state. Near 1: more on future state.
    epsilon = 1             # 1 = 100% random actions

    # Array to keep track of the number of steps per episode for the robot to find the target.
    # We know that the robot will inevitably find the target, so the reward is always obtained,
    # so we want to know if the robot is reaching the target efficiently.
    steps_per_episode = np.zeros(episodes)

    step_count=0
    for i in range(episodes):
        
        # Reset environment at teh beginning of episode
        state = env.reset()[0]
        terminated = False

        # Robot keeps going until it finds the target
        while(not terminated):

            # Select action based on epsilon-greedy
            if  random.random() < epsilon:
                # select random action
                action = env.action_space.sample()
            else:                
                # Convert state of [1,2,3,4] to (1,2,3,4), use this to index into the 4th dimension of the 5D array.
                q_state_idx = tuple(state) 

                # select best action
                action = np.argmax(q[q_state_idx])
            
            # Perform action
            new_state,reward,terminated,_,_ = env.step(action)

            # Convert state of [1,2,3,4] and action of [1] into (1,2,3,4,1), use this to index into the 5th dimension of the 5D array.
            q_state_action_idx = tuple(state) + (action,)

            # Convert new_state of [1,2,3,4] into (1,2,3,4), use this to index into the 4th dimension of the 5D array.
            q_new_state_idx = tuple(new_state)

            
            # Update Q-Table
            q[q_state_action_idx] = q[q_state_action_idx] + learning_rate_a * (
                        reward + discount_factor_g * np.max(q[q_new_state_idx]) - q[q_state_action_idx]
                )

            # Update current state
            state = new_state

            # Record steps
            step_count+=1
            if terminated:
                steps_per_episode[i] = step_count
                step_count = 0

        # Decrease epsilon
        epsilon = max(epsilon - 1/episodes, 0)

    env.close()

  
    # Save Q Table
    f = open("v0_mazerunner_solution.pkl","wb")
    pickle.dump(q, f)
    f.close()
        
######################################
# run q-learning a number of episods
def playModelMove(env,q,episodes):
    
    
    steps_per_episode = np.zeros(episodes)

    step_count=0
    for i in range(episodes):
       

        # Reset environment at teh beginning of episode
        state = env.reset()[0]
        terminated = False

        env.render()
        print(f'Episode {i}')
        # Robot keeps going until it finds the target
        while(not terminated):
            time.sleep(0.5)
                            
            # Convert state of [1,2,3,4] to (1,2,3,4), use this to index into the 4th dimension of the 5D array.
            q_state_idx = tuple(state) 

            # select best action
            action = np.argmax(q[q_state_idx])
            
            # Perform action
            new_state,reward,terminated,_,_ = env.step(action)

            
            # Update current state
            state = new_state

            # Record steps
            step_count+=1
            if terminated:
                print("Episod ",i," step count : ",step_count)
                step_count = 0
    

    env.close()
            
######################################
# Test using Q learning. 
def test_q_learning(episodes,render=True):

    env = gym.make('maze-runner-v0', render_mode='human')

    # Load Q Table from file.
    f = open('v0_mazerunner_solution.pkl', 'rb')
    q = pickle.load(f)
    f.close()

  
    # Start game
    t = threading.Thread(target=playModelMove, args=(env,q,episodes))
    t.daemon = True
    t.start()
    
    env.unwrapped.start() # Start the environment's main loop
    
######################################
if __name__ == '__main__':

    # Train/test using Q-Learning
    #train_q_learning(1000,  render=False)
    test_q_learning(5,  render=True)

