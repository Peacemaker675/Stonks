import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    def __init__(self, df, window_size = 60):
        self.df = df
        self.window_size = window_size
        self.balance = 1000000
        self.shares = 0
        self.unrealized = 0
        self.current_price = 0
        self.action_space = spaces.Discrete(3) # buy 0, sell 1, hold 2
        self.observation_space = spaces.Box( 
            low= -np.inf, high= np.inf,
            shape= (window_size, 14), dtype=np.float32 # shape = 60 mins of past data * attributes
        )

    def reset(self, *, seed = None, options = None):
        super().reset(seed=seed, options=options)
        self.current_step = self.window_size
        return self._get_observation()
    
    def step(self, action):
        if action == 0:
            pass
        elif action == 1:
            pass
        else:
            pass

    def _get_observation(self):
        curr_point = self.df.iloc[self.current_step - self.window_size : self.current_step].values
        self.current_price = curr_point[59][4] # close of last point
        return curr_point
    
