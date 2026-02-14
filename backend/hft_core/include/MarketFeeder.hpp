#pragma once
#include "Types.hpp"
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <iostream>

class MarketFeeder {
public:
    MarketFeeder(const std::string& filepath) : filepath_(filepath) {}

    bool loadData() {
        std::ifstream file(filepath_);
        if (!file.is_open()) {
            std::cerr << "Error: Could not open " << filepath_ << std::endl;
            return false;
        }

        std::string line;
        // Skip Header
        std::getline(file, line); 

        while (std::getline(file, line)) {
            ticks_.push_back(parseLine(line));
        }
        return true;
    }

    const std::vector<MarketTick>& getTicks() const { return ticks_; }

private:
    std::string filepath_;
    std::vector<MarketTick> ticks_;

    MarketTick parseLine(const std::string& line) {
        std::stringstream ss(line);
        std::string token;
        std::vector<double> raw_values;
        
        // 1. Split CSV line into doubles
        while (std::getline(ss, token, ',')) {
            try { 
                if(!token.empty()) raw_values.push_back(std::stod(token)); 
                else raw_values.push_back(0.0);
            } catch (...) { 
                raw_values.push_back(0.0); 
            }
        }

        MarketTick tick;
        if (raw_values.empty()) return tick;

        // 2. Extract Timestamp (Column 0)
        tick.timestamp = static_cast<long>(raw_values[0]);

        // 3. Extract Price (Column 4 = Close) for execution logic
        // Ensure we have enough columns to avoid crashes
        if (raw_values.size() > 5) {
            tick.price = raw_values[4]; 
        } else {
            tick.price = 0.0;
        }

        // 4. Populate Features Vector (Columns 1 to 17)
        // We need exactly 17 features for the model. 
        // We skip the timestamp (col 0) and take the next 17 columns.
        // You might need to adjust the start index '1' depending on exactly which columns your model trained on.
        int start_col = 1; 
        int feature_count = 14;

        for (int i = 0; i < feature_count; ++i) {
            if (start_col + i < raw_values.size()) {
                tick.features.push_back(static_cast<float>(raw_values[start_col + i]));
            } else {
                tick.features.push_back(0.0f); // Pad with 0 if data is missing
            }
        }
        return tick;
    }
};