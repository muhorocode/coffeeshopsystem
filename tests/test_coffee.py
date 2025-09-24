import pytest

from coffee import Coffee
from order import Order


@pytest.fixture(autouse=True)
def clear_all_orders():
    # Ensure Order.all_orders exists and is cleared before each test
    original = getattr(Order, "all_orders", None)
    Order.all_orders = []
    yield
    if original is None:
        delattr(Order, "all_orders")
    else:
        Order.all_orders = original


class SimpleOrder:
    def __init__(self, coffee, customer, price):
        self.coffee = coffee
        self.customer = customer
        self.price = price


def add_order(coffee, customer, price):
    o = SimpleOrder(coffee, customer, price)
    Order.all_orders.append(o)
    return o


def test_orders_filters_by_coffee_instance():
    latte = Coffee("Latte")
    espresso = Coffee("Espresso")

    o1 = add_order(latte, "Alice", 3.0)
    o2 = add_order(espresso, "Bob", 4.0)
    o3 = add_order(latte, "Carol", 5.0)

    orders_for_latte = latte.orders()
    assert set(orders_for_latte) == {o1, o3}
    assert o2 not in orders_for_latte


def test_customers_returns_unique_customers_for_coffee():
    mocha = Coffee("Mocha")
    add_order(mocha, "Alice", 3.0)
    add_order(mocha, "Alice", 4.0)
    add_order(mocha, "Bob", 5.0)

    customers = mocha.customers()
    assert set(customers) == {"Alice", "Bob"}
    assert len(customers) == 2


def test_average_price_computed_and_rounded_to_two_decimals():
    americano = Coffee("Americano")
    prices = [1.99, 2.01, 2.02]  # average ~ 2.006666..., rounds to 2.01
    for p in prices:
        add_order(americano, "Cust", p)

    expected = round(sum(prices) / len(prices), 2)
    assert americano.average_price() == expected


def test_init_raises_for_non_string_or_short_name():
    with pytest.raises(Exception) as e1:
        Coffee(123)
    assert "Coffee name must be a string with at least 3 characters" in str(e1.value)

    with pytest.raises(Exception) as e2:
        Coffee("ab")
    assert "Coffee name must be a string with at least 3 characters" in str(e2.value)


def test_no_orders_returns_zero_counts_and_average():
    cappuccino = Coffee("Cappuccino")
    assert cappuccino.num_orders() == 0
    assert cappuccino.average_price() == 0


def test_orders_and_customers_scoped_by_instance_with_same_name():
    fw1 = Coffee("Flat White")
    fw2 = Coffee("Flat White")  # same name, different instances

    o1 = add_order(fw1, "Alice", 3.5)
    o2 = add_order(fw1, "Bob", 4.0)
    o3 = add_order(fw2, "Charlie", 3.0)
    o4 = add_order(fw2, "Alice", 3.2)

    assert set(fw1.orders()) == {o1, o2}
    assert set(fw2.orders()) == {o3, o4}

    assert set(fw1.customers()) == {"Alice", "Bob"}
    assert set(fw2.customers()) == {"Charlie", "Alice"}