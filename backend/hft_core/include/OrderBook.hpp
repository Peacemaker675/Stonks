#pragma once
#include "Types.hpp"
#include <vector>
#include <iostream>

struct Level { double price; double qty; };

class OrderBook {
public:
    void update(double price, double volatility);
    double getExecutionPrice(int side, double qty);

private:
    std::vector<Level> bids_;
    std::vector<Level> asks_;
    double current_price_;
};