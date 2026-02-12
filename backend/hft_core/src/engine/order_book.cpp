// ERROR WAS HERE: Changed form "../../include/..." to just "engine/..."
#include "engine/order_book.h"

void OrderBook::add_order(int id, double price, double quantity, bool is_buy) {
  std::lock_guard<std::mutex> lock(book_mutex);
  Order order{id, price, quantity, is_buy, 0};

  if (is_buy) {
    bids[price].push_back(order);
  } else {
    asks[price].push_back(order);
  }
}

void OrderBook::cancel_order(int id) {
  std::lock_guard<std::mutex> lock(book_mutex);

  auto remove_from_map = [id](auto &map) {
    for (auto &[price, list] : map) {
      auto it = list.begin();
      while (it != list.end()) {
        if (it->id == id) {
          list.erase(it);
          return true;
        }
        ++it;
      }
    }
    return false;
  };

  if (!remove_from_map(bids)) {
    remove_from_map(asks);
  }
}

std::pair<double, double> OrderBook::get_top_of_book() const {
  std::lock_guard<std::mutex> lock(book_mutex);

  double best_bid = bids.empty() ? 0.0 : bids.begin()->first;
  double best_ask = asks.empty() ? 0.0 : asks.begin()->first;

  return {best_bid, best_ask};
}

double OrderBook::get_spread() const {
  auto top = get_top_of_book();
  if (top.first == 0.0 || top.second == 0.0)
    return -1.0;
  return top.second - top.first;
}

std::string OrderBook::print_book() const {
  std::stringstream ss;
  auto top = get_top_of_book();
  ss << "Spread: " << (top.second - top.first) << "\n";
  ss << "Best Bid: " << top.first << " | Best Ask: " << top.second;
  return ss.str();
}
