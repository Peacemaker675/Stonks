#pragma once
#include <vector>
#include <string>
#include <iostream>

struct MarketTick {
    long timestamp;
    
    // The model expects a vector of 17 floats
    std::vector<float> features; 
    
    // We keep 'price' separate because the Strategy needs it for PnL calculation
    double price; 
};

struct Order {
    std::string id;
    int side; // 0=Buy, 1=Sell
    double price;
    double quantity;
};