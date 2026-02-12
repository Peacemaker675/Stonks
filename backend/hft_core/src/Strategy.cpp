#include "Strategy.hpp"
#include <iostream>

Strategy::Strategy(std::shared_ptr<PPOModel> model, std::shared_ptr<OrderBook> book)
    : model_(model), book_(book) {}

void Strategy::onTick(const MarketTick& tick) {
    // 1. Update Market Internals
    // Assuming feature[7] is volatility (based on your JSON list)
    double vol = (tick.features.size() > 7) ? tick.features[7] : 0.01;
    book_->update(tick.price, vol);

    // 2. Maintain Rolling Buffer (FIFO)
    history_buffer_.push_back(tick.features);
    if(history_buffer_.size() > REQUIRED_STEPS) {
        history_buffer_.pop_front();
    }

    // 3. Warmup Check
    if(history_buffer_.size() < REQUIRED_STEPS) {
        if(history_buffer_.size() % 10 == 0) 
            std::cout << "[Warmup] " << history_buffer_.size() << "/60 ticks collected...\r";
        return;
    }

    // 4. Flatten Data for ONNX
    std::vector<float> input_flat;
    input_flat.reserve(REQUIRED_STEPS * FEATURE_DIM);
    for(const auto& f : history_buffer_) {
        input_flat.insert(input_flat.end(), f.begin(), f.end());
    }

    // 5. INFERENCE
    int action = model_->predict(input_flat);

    // 6. EXECUTION LOGIC
    if(action == 0) { // BUY
        double price = book_->getExecutionPrice(0, 1.0);
        if(cash_ > price) {
            cash_ -= price;
            position_ += 1.0;
            std::cout << ">>> BUY @ " << price << " | PnL: " << (cash_ + (position_ * price) - 100000) << std::endl;
        }
    } else if(action == 1) { // SELL
        if(position_ > 0) {
            double price = book_->getExecutionPrice(1, 1.0);
            cash_ += price;
            position_ -= 1.0;
            std::cout << ">>> SELL @ " << price << " | PnL: " << (cash_ + (position_ * price) - 100000) << std::endl;
        }
    }
    // Action 2 is HOLD (do nothing)
}