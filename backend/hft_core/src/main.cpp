#include "MarketFeeder.hpp"
#include "OrderBook.hpp"
#include "PPOModel.hpp"
#include "Strategy.hpp"
#include <memory>
#include <iostream>

int main() {
    try {
        std::cout << "[HFT] System Starting...\n";

        // 1. Initialize Components
        auto model = std::make_shared<PPOModel>("models/ppo_hft.onnx");
        auto book = std::make_shared<OrderBook>();
        
        // 2. Initialize Feeder
        MarketFeeder feeder("data/market_data.csv");
        
        // 3. Initialize Strategy
        Strategy strategy(model, book);

        // 4. Load Data
        std::cout << "[HFT] Loading Market Data...\n";
        if (!feeder.loadData()) {
            return -1;
        }
        
        const auto& ticks = feeder.getTicks();
        std::cout << "[HFT] Loaded " << ticks.size() << " ticks.\n";

        // 5. Run Loop
        for(const auto& tick : ticks) {
            strategy.onTick(tick);
        }

    } catch (const std::exception& e) {
        std::cerr << "[ERROR] " << e.what() << std::endl;
        return -1;
    }
    return 0;
}