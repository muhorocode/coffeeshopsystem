import pytest

from customer import Customer
from order import Order


@pytest.fixture(autouse=True)
def reset_order_registry():
    # Ensure a clean Order registry before each test
    if not hasattr(Order, "all_orders"):
        Order.all_orders = []
    else:
        Order.all_orders = []


class TestCustomer:
    def test_customer_init_with_valid_name_sets_and_gets_name(self):
        c = Customer("Alice")
        assert c.name == "Alice"

    def test_create_order_links_to_customer_and_is_listed_in_orders(self):
        c = Customer("Bob")
        order = c.create_order("Latte", 3.5)

        assert isinstance(order, Order)
        assert order.customer is c
        assert order in c.orders()

        # Ensure another customer's orders are not included
        other = Customer("Eve")
        assert order not in other.orders()

    def test_coffees_returns_unique_coffees_for_customer(self):
        c1 = Customer("Cara")
        c2 = Customer("Dave")

        # Multiple orders including duplicates for c1
        c1.create_order("Latte", 4.0)
        c1.create_order("Espresso", 3.0)
        c1.create_order("Latte", 4.5)  # duplicate coffee
        # Orders for another customer should not affect c1's coffees
        c2.create_order("Mocha", 5.0)
        c2.create_order("Latte", 4.0)

        coffees_c1 = c1.coffees()
        assert set(coffees_c1) == {"Latte", "Espresso"}
        # Ensure deduplication
        assert len(coffees_c1) == 2

    def test_init_with_empty_name_raises_exception(self):
        with pytest.raises(Exception) as exc:
            Customer("")
        assert "Name must be a string between 1 and 15 characters" in str(exc.value)

    def test_init_with_overlength_name_raises_exception(self):
        with pytest.raises(Exception) as exc:
            Customer("A" * 16)
        assert "Name must be a string between 1 and 15 characters" in str(exc.value)

    def test_init_with_non_string_name_raises_exception(self):
        with pytest.raises(Exception) as exc:
            Customer(123)
        assert "Name must be a string between 1 and 15 characters" in str(exc.value)