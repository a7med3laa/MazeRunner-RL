# MazeRunner-RL

- The MazeRunner game is a custom Gymnasium environment example used for Reinforcement learning to train and test an agent. The game is simple Where there is a robot that searches for a way to win the diamond. Moreover, the robot tries to avoid objects to not lose.

- The environment is solved using both stable_baselines3 A2C Algorithm and Q-learning 

<img width="308" alt="Capture" src="https://github.com/user-attachments/assets/148567b0-105c-407b-8d68-371b5690a01e" />


# Libraries used in the project:
1. Tkinter
2. Gymnasium 1.0.0
3. Stable_baselines3 2.3.2




# Files in the project:
1. MazeRunner.py: The class of simple Tkinter game
2. play.py: Let the user play MazeRunner by moving in all four directions using the keyboard (up, down, right, left)
3. play_random.py: Make the agent take a random move in any direction and play the game and if it hits an object it loses and starts the game again.
4. MaveRunner_Gymnisuim_Env.py: use the Gymnasium API to make a standard environment that can be used by the RL agent.
5. q_learning.py: solve MazeRunner environment using Q-learning. there are two functions to learn and to test algorithm
6. A2C_Model.py: solve MazeRunner environment using Stable_baselines3 A2C algorithm. there are two functions to learn and to test algorithm
