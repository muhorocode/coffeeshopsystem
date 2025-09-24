import pytest

from order import Order


@pytest.fixture(autouse=True)
def reset_all_orders():
    Order.all_orders.clear()
    yield
    Order.all_orders.clear()


class TestOrder:
    def test_order_creation_with_valid_price_sets_properties_and_registers_instance(self):
        customer = "Alice"
        coffee = "Latte"
        price = 5.5

        order = Order(customer, coffee, price)

        assert order.customer == customer
        assert order.coffee == coffee
        assert order.price == price
        assert len(Order.all_orders) == 1
        assert Order.all_orders[0] is order

    def test_price_accepts_boundary_values_1_0_and_10_0(self):
        o1 = Order("Cust1", "Coffee1", 1.0)
        o2 = Order("Cust2", "Coffee2", 10.0)

        assert o1.price == 1.0
        assert o2.price == 10.0
        assert Order.all_orders == [o1, o2]

    def test_all_orders_accumulates_multiple_order_instances(self):
        o1 = Order("C1", "Espresso", 1.0)
        o2 = Order("C2", "Cappuccino", 2.5)
        o3 = Order("C3", "Americano", 3.75)

        assert Order.all_orders == [o1, o2, o3]

    @pytest.mark.parametrize("invalid_price", ["five", None, object()])
    def test_init_raises_for_non_numeric_price(self, invalid_price):
        with pytest.raises(Exception, match="price must be a number between 1.0 and 10.0"):
            Order("Cust", "Coffee", invalid_price)

    @pytest.mark.parametrize("invalid_price", [0.0, 0.99, 10.0001, 100])
    def test_init_raises_for_price_out_of_range(self, invalid_price):
        with pytest.raises(Exception, match="price must be a number between 1.0 and 10.0"):
            Order("Cust", "Coffee", invalid_price)

    def test_invalid_initialization_does_not_append_to_all_orders(self):
        with pytest.raises(Exception):
            Order("Cust", "Coffee", "invalid")
        assert len(Order.all_orders) == 0