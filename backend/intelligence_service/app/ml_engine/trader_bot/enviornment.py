import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt

class TradingEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, df, window_size=60, render_mode=None):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.window_size = window_size
        self.render_mode = render_mode
        self.prev_price = 0
        self.initial_balance = 1_000_000_000 # 10 crore !!!
        self.balance = self.initial_balance
        self.shares = 0

        self.current_step = None
        self.current_price = None
        self.current_vol = None

        self.action_space = spaces.Discrete(3)  # 0 buy, 1 sell, 2 hold
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(window_size, self.df.shape[1] + 3),
            dtype=np.float32,
        )

        self.history = {"price": [], "net_worth": [], "action": [], "balance": []}

        self.fig = None
        self.ax1 = None
        self.ax2 = None

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.balance = self.initial_balance
        self.shares = 0
        self.current_step = self.window_size
        self.prev_price = 0
        self.history = {"price": [], "net_worth": [], "action": [], "balance": []}

        obs = self._get_observation()
        return obs, {}

    def step(self, action):
        current_action = -1
        self.current_step += 1
        obs = self._get_observation()
        prev_balance = self.balance
        prev_net_worth = self.balance + self.shares * self.current_price
        trade_size = int(0.15 * self.current_vol)
        max_exposure = 0.7 * self.initial_balance
        current_exposure = self.shares * self.current_price
        reward = 0
        if action == 0 and current_exposure < max_exposure:  # BUY
            max_affordable = int(self.balance // self.current_price)
            shares_to_buy = min(trade_size, max_affordable)
            cost = shares_to_buy * self.current_price

            if shares_to_buy > 0:
                current_action = action
                self.balance -= cost
                self.shares += shares_to_buy
            else:
                reward -= 0.001

        elif action == 1:  # SELL
            
            shares_to_sell = self.shares
            revenue = shares_to_sell * self.current_price

            if shares_to_sell > 0:
                current_action = action
                self.balance += revenue
                self.shares -= shares_to_sell
            else:
                reward -= 0.001

        # reward
        current_net_worth = self.balance + self.shares * self.current_price

        reward += np.log(current_net_worth / prev_net_worth)
        reward += (self.balance - prev_balance) / current_net_worth
        if(self.balance == prev_balance):
            reward -= 0.1
        terminated = current_net_worth < 0.8 * self.initial_balance
        truncated = (
            self.current_step >= len(self.df) - 1
            or self.current_step % 2000 == 0
        )
        # logging
        self.history["price"].append(self.current_price)
        self.history["balance"].append(self.balance)
        self.history["net_worth"].append(current_net_worth)
        self.history["action"].append(current_action)

        return obs, reward, terminated, truncated, {"balance":self.balance}

    def _get_observation(self):
        window = self.df.iloc[
            self.current_step - self.window_size : self.current_step
        ].values.astype(np.float32)

        self.prev_price = self.current_price
        self.current_price = window[-1][3]
        self.current_vol = max(window[-1][4], 1)

        cash_ratio = self.balance / self.initial_balance
        position_value = (self.shares * self.current_price) / self.initial_balance
        position_ratio = self.shares / 1e6  # scale

        agent_state = np.array(
            [cash_ratio, position_value, position_ratio],
            dtype=np.float32
        )

        agent_state = np.tile(agent_state, (self.window_size, 1))

        return np.concatenate([window, agent_state], axis=1)


    def render(self):
        if self.render_mode != "human":
            return

        if self.fig is None:
            plt.ion()
            self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, sharex=True)

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.ax1.plot(self.history["price"], label="Price")
        for i, a in enumerate(self.history["action"]):
            if a == 0:
                self.ax1.scatter(i, self.history["price"][i], c="green", marker="^")
            elif a == 1:
                self.ax1.scatter(i, self.history["price"][i], c="red", marker="v")

        self.ax2.plot(self.history["net_worth"], label="Net Worth", color="black")

        balance_history = np.array(self.history["balance"])
        growth_percentage = (balance_history - self.initial_balance) / self.initial_balance * 100
        self.ax3.plot(growth_percentage, label="Cash Growth (%)", color="blue")
        self.ax3.set_ylabel("Profit %")

        self.ax1.legend()
        self.ax2.legend()
        self.ax3.legend()

        plt.pause(0.001)
