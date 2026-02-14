#pragma once
#include "Types.hpp"
#include <vector>
#include <iostream>

struct Level { double price; double qty; };

class OrderBook {
public:
    void update(double price, double volume, double volatility);
    double getExecutionPrice(int side, double qty);

private:
    double current_price_ = 0;
    double current_volume_ = 100000;
    double current_volatility_ = 0.01;
};