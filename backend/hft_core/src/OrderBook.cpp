#include "OrderBook.hpp"
#include <cmath>

void OrderBook::update(double price, double volume, double volatility) {
    current_price_ = price;
    current_volume_ = volume;
    // If volatility is 0 in CSV, default to 1% (0.01)
    current_volatility_ = (volatility > 0) ? volatility : 0.01;
}

// Calculate the Price you actually get (including synthetic spread & slippage)
double OrderBook::getExecutionPrice(int side, double order_size) {
    // 1. Base Spread (e.g., 0.02% or 2 basis points)
    // In high vol, spread widens (Standard HFT behavior)
    double spread_pct = 0.0002 + (current_volatility_ * 0.1); 
    double half_spread = current_price_ * (spread_pct / 2.0);

    // 2. Market Impact (Slippage)
    // If we buy 1% of the total volume, we move price by ~1% of volatility
    double market_impact = 0.0;
    if (current_volume_ > 0) {
        double participation_rate = order_size / current_volume_;
        market_impact = current_price_ * current_volatility_ * participation_rate;
    }
    // 3. Final Price Calculation
    if (side == 0) { // BUY
        // You pay: Price + Half Spread + Impact
        return current_price_ + half_spread + market_impact;
    } else { // SELL
        // You get: Price - Half Spread - Impact
        return current_price_ - half_spread - market_impact;
    }
}