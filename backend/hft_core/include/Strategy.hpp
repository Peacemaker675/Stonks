#pragma once
#include "PPOModel.hpp"
#include "OrderBook.hpp"
#include "Types.hpp"
#include <deque>
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
    double cash_ = 100000.0;
    double position_ = 0.0;
};