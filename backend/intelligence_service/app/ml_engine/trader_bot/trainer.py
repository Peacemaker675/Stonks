import pandas as pd
from stable_baselines3 import PPO
from enviornment import TradingEnv

data = pd.read_csv("training.csv")
data = data.drop(columns=["date"])

env = TradingEnv(data)

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    n_steps=2048,
    batch_size=256,
    learning_rate=3e-4,
)

model.learn(total_timesteps=300_000)
model.save("ppo_trader")
