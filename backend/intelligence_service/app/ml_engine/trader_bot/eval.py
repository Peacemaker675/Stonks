import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from enviornment import TradingEnv

data = pd.read_csv("training.csv")
data = data.iloc[200000:].reset_index(drop=True)
data = data.drop(columns=["date"], errors='ignore')

env = DummyVecEnv([lambda: TradingEnv(data, render_mode="human")])

try:
    env = VecNormalize.load("model/vec_normalize_v2.pkl", env)
except FileNotFoundError:
    print("file not found")
    exit()

env.training = False 
env.norm_reward = False

model = PPO.load("model/ppo_trader_v2", env=env)
obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    print(f"balance = {info[0]["balance"]}")
    env.render()
    if done:
        break