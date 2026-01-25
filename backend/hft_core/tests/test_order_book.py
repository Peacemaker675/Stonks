import pytest
import hft_engine

@pytest.fixture
def book():
    """Setup a fresh OrderBook for every test function"""
    return hft_engine.OrderBook()

def test_add_orders(book):
    # Buy Order @ 100.5
    book.add_order(1, 100.5, 10, True)
    # Sell Order @ 101.0
    book.add_order(2, 101.0, 5, False)
    
    top = book.get_top_of_book()
    assert top == (100.5, 101.0)
    assert book.get_spread() == 0.5

def test_execution_logic(book):
    """Test that spread calculates correctly under pressure"""
    book.add_order(1, 100.0, 10, True)
    book.add_order(2, 105.0, 10, False)
    assert book.get_spread() == 5.0
    
    # Add a better bid
    book.add_order(3, 102.0, 5, True)
    assert book.get_spread() == 3.0 # (105.0 - 102.0)

def test_cancel_order(book):
    book.add_order(1, 100.0, 10, True)
    book.add_order(2, 101.0, 10, False)
    
    book.cancel_order(1)
    
    # After cancel, best bid should be 0.0 (empty)
    top = book.get_top_of_book()
    assert top[0] == 0.0