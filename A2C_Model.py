'''
Example of using Q-Learning or StableBaseline3 to train our custom environment.
'''
import time
import threading
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
from stable_baselines3 import A2C
import os
import MaveRunner_Gymnisuim_Env # Even though we don't use this class here, we should include it here so that it registers the WarehouseRobot environment.

######################################

# Train using StableBaseline3. Lots of hardcoding for simplicity i.e. use of the A2C (Advantage Actor Critic) algorithm.
def train_sb3():
    # Where to store trained model and logs
    models_dir = "models/A2C"
    logdir = "logs"
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    env = gym.make('maze-runner-v0')
    env.reset()
    
    # Use Advantage Actor Critic (A2C) algorithm.
    # Use MlpPolicy for observation space 1D vector.
    model = A2C('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
   
    
    # This loop will keep training until you stop it with Ctr-C.
    # Start another cmd prompt and launch Tensorboard: tensorboard --logdir logs
    # Once Tensorboard is loaded, it will print a URL. Follow the URL to see the status of the training.
    # Stop the training when you're satisfied with the status.
    TIMESTEPS = 10000
    
    for i in range(10):
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="A2C")
        model.save(f"{models_dir}/a2c_{TIMESTEPS*i}")

    env.close()

######################################

def playModelMove(env,model):
    # Play 5 episods
    episods=2
    
    # Run a test
    obs = env.reset()[0]
    terminated = False
    
    
    while episods:
        env.render()
        print("episods = ",episods)
        
        time.sleep(0.5)
        
        action, _ = model.predict(observation=obs, deterministic=False) # Turn on deterministic, so predict always returns the same behavior
        obs, _, terminated, _, _ = env.step(action)

        if terminated:
            episods-=1
            obs = env.reset()[0]
    env.close()
            
######################################
# Test using StableBaseline3. Lots of hardcoding for simplicity.
def test_sb3(render=True):

    env = gym.make('maze-runner-v0', render_mode='human')

    # Load model
    model = A2C.load('models/A2C/a2c_110000', env=env)
  
    # Start game
    t = threading.Thread(target=playModelMove, args=(env,model))
    t.daemon = True
    t.start()
    
    env.unwrapped.start() # Start the environment's main loop 
    
######################################    
if __name__ == '__main__':

   
    # Train using StableBaseline3
    #train_sb3()
    
    # Test using StableBaseline3
    test_sb3()
