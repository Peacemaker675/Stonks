#pragma once
#include <iostream>
#include <limits>
#include <map>
#include <mutex>
#include <sstream>
#include <string>
#include <vector>

// Order structure
struct Order {
  int id;
  double price;
  double quantity;
  bool is_buy; // true = Buy, false = Sell
  long long timestamp;
};

class OrderBook {
private:
  // Price -> List of Orders.
  // Bids (Buy): Descending order (Highest price first)
  // Asks (Sell): Ascending order (Lowest price first)
  std::map<double, std::vector<Order>, std::greater<double>> bids;
  std::map<double, std::vector<Order>, std::less<double>> asks;

  mutable std::mutex book_mutex; // Thread safety

public:
  OrderBook() = default;

  void add_order(int id, double price, double quantity, bool is_buy);
  void cancel_order(int id);

  // Returns (best_bid, best_ask)
  std::pair<double, double> get_top_of_book() const;

  // Returns current spread
  double get_spread() const;

  // For debugging/visualization
  std::string print_book() const;
};
