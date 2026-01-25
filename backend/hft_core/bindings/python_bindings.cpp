#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
// ERROR WAS HERE: Changed form "../../include/..." to just "engine/..."
#include "engine/order_book.h" 

namespace py = pybind11;

PYBIND11_MODULE(hft_engine, m) {
    m.doc() = "Hybrid HFT Engine Core optimized in C++";

    py::class_<OrderBook>(m, "OrderBook")
        .def(py::init<>())
        .def("add_order", &OrderBook::add_order, "Add a limit order")
        .def("cancel_order", &OrderBook::cancel_order, "Cancel an order by ID")
        .def("get_top_of_book", &OrderBook::get_top_of_book, "Get Best Bid/Ask")
        .def("get_spread", &OrderBook::get_spread, "Get current spread")
        .def("print_book", &OrderBook::print_book, "Debug string of book");
}