import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from enviornment import TradingEnv  

data = pd.read_csv("training.csv")
data = data.iloc[:200_000].copy() 
data = data.drop(columns=["date"], errors='ignore')
    
env = DummyVecEnv([lambda: TradingEnv(data)])

env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.)

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    n_steps=2048,
    batch_size=256,
    learning_rate=3e-4,
    max_grad_norm=0.5 
)

print("Starting training...")
try:
    model.learn(total_timesteps=200_000)
    print("Training finished.")
except Exception as e:
    print(f"Training failed with error: {e}")

model.save("model/ppo_trader_v2")
env.save("model/vec_normalize_v2.pkl") 
print("Model and stats saved.")