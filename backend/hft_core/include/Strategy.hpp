#pragma once
#include "PPOModel.hpp"
#include "OrderBook.hpp"
#include "Types.hpp"
#include <deque>
#include <iomanip>
#include <iostream>
#include <memory>

class Strategy {
public:
    Strategy(std::shared_ptr<PPOModel> model, std::shared_ptr<OrderBook> book);
    void onTick(const MarketTick& tick);

private:
    std::shared_ptr<PPOModel> model_;
    std::shared_ptr<OrderBook> book_;
    
    // Rolling Buffer for Time Series (60 steps)
    std::deque<std::vector<float>> history_buffer_;
    const size_t REQUIRED_STEPS = 60;
    const size_t FEATURE_DIM = 17;

    // Portfolio State
    double initial_cash = 1'000'000'000.0;
    double cash_ = initial_cash;
    double shares = 0;
    double profit = 0;

    /*
        cash_ratio = self.balance / self.initial_balance
        position_value = (self.shares * self.current_price) / self.initial_balance
        position_ratio = self.shares / 1e6  # scale
    */
};