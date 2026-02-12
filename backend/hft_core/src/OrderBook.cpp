#include "OrderBook.hpp"
#include <cmath>

void OrderBook::update(double price, double volatility) {
    current_price_ = price;
    bids_.clear();
    asks_.clear();

    // HFT Simulation: Spread widens with volatility
    // Base spread 1 pip (0.0001) + volatility impact
    double spread = 0.0001 + (volatility * 0.01); 

    for(int i=1; i<=5; ++i) {
        bids_.push_back({price - (spread * i), 1000.0 / i});
        asks_.push_back({price + (spread * i), 1000.0 / i});
    }
}

double OrderBook::getExecutionPrice(int side, double qty) {
    // 0 = Buy (Ask side), 1 = Sell (Bid side)
    // Simple top-of-book simulation for now
    if (side == 0 && !asks_.empty()) return asks_[0].price;
    if (side == 1 && !bids_.empty()) return bids_[0].price;
    return current_price_;
}