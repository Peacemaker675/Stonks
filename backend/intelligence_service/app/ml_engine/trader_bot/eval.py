import pandas as pd
from stable_baselines3 import PPO
from enviornment import TradingEnv

data = pd.read_csv("training.csv")
data = data.drop(columns=["date"])

env = TradingEnv(data, render_mode="human")
model = PPO.load("ppo_trader")

obs, _ = env.reset()

while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    env.render()

    if terminated or truncated:
        break
