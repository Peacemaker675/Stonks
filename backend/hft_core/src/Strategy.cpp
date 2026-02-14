#include "Strategy.hpp"

Strategy::Strategy(std::shared_ptr<PPOModel> model, std::shared_ptr<OrderBook> book)
    : model_(model), book_(book) {}

void Strategy::onTick(const MarketTick& tick) {
    // 1. Update Market Internals
    // Assuming feature[6] is volatility (based on your JSON list)

    std::cout << std::fixed << std::setprecision(2);

    double volatility = (tick.features.size() > 7) ? tick.features[5] : 0.01;
    double current_price = tick.features[3];
    double volume = tick.features[4];

    book_->update(current_price, volume, volatility);

    double cash_ratio = cash_ / initial_cash;
    double position_value = (shares * current_price) / initial_cash;
    double position_ratio = shares / 1e6;  // scale
    std::vector<float> current_observation = tick.features;
    current_observation.push_back(static_cast<float>(cash_ratio));
    current_observation.push_back(static_cast<float>(position_value));
    current_observation.push_back(static_cast<float>(position_ratio));
    // 2. Maintain Rolling Buffer (FIFO)
    history_buffer_.push_back(current_observation);
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
        double order_size = cash_ * 0.3 / current_price;
        double price = book_->getExecutionPrice(0, order_size);
        if(cash_ > price){
            cash_ -= price * order_size;
            shares += order_size;
            double net_worth = profit + cash_ + (shares * current_price);
            std::cout << ">>> BUY @ " << price << " | CASH: " << (cash_) << " | PROFIT: "<< profit << " | NETWORTH: "<< net_worth << std::endl;
        } 
    } else if(action == 1) { // SELL
        if(shares > 0) {
            double price = book_->getExecutionPrice(1, shares);
            cash_ += price * shares;
            if(cash_ > initial_cash){
                profit = cash_ - initial_cash;
                cash_ = initial_cash; // Reset cash to initial after taking profit
            }
            shares = 0;
            std::cout << ">>> SELL @ " << price << " | CASH: " << (cash_) << " | PROFIT: " << profit << std::endl;
        }// Action 2 is HOLD (do nothing)
    }
}