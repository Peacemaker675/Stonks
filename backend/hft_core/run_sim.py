import pandas as pd
import time
import hft_engine  # <--- This is your compiled C++ Code!

# 1. Configuration
DATA_PATH = "training.csv"
SIMULATION_SPEED = 0.01  # Delay in seconds (to see it happen)


def run_hft_simulation():
    print("--- 🚀 Starting Hybrid HFT Simulation ---")

    # 2. Load Data
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"✅ Loaded {len(df)} rows of market data.")
    except FileNotFoundError:
        print(
            "❌ Error: Data file not found. Run the export script from the previous step first!"
        )
        return

    # 3. Initialize the C++ Engine
    # This object lives in C++ memory (Super fast)
    order_book = hft_engine.OrderBook()

    print("\nStarting Feed Replay...")

    # 4. The Event Loop (Simulating a Trading Session)
    # We will simulate the last 100 rows to keep it short
    recent_data = df.head(100).reset_index(drop=True)

    for index, row in recent_data.iterrows():
        price = row["close"]
        timestamp = row["date"]

        # --- A. SIMULATE MARKET MAKER STRATEGY ---
        # We place a Bid slightly below price and Ask slightly above
        bid_price = round(price - 0.50, 2)
        ask_price = round(price + 0.50, 2)

        # Send to C++ Core
        # ID, Price, Qty, Is_Buy (1=Buy, 0=Sell)
        order_book.add_order(index * 2, bid_price, 10, True)  # Buy Order
        order_book.add_order(index * 2 + 1, ask_price, 10, False)  # Sell Order

        # --- B. QUERY C++ CORE ---
        # Retrieve the current state from C++ memory
        spread = order_book.get_spread()
        top_bid, top_ask = order_book.get_top_of_book()

        # --- C. VISUALIZATION ---
        print(
            f"[{timestamp}] Market: {price} | C++ Book: {top_bid} x {top_ask} | Spread: {spread:.2f}"
        )

        # Cleanup (Simple logic: Cancel old orders to keep book fresh)
        if index > 0:
            order_book.cancel_order((index - 1) * 2)
            order_book.cancel_order((index - 1) * 2 + 1)

        time.sleep(SIMULATION_SPEED)

    print("\n--- ✅ Simulation Complete ---")


if __name__ == "__main__":
    run_hft_simulation()

