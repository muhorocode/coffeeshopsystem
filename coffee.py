# import Order from order to search through orders
from order import Order

class Coffee:
    def __init__(self,name):
        if not isinstance(name,str) or len(name) <3:
            raise Exception('Coffee name must be a string with at least 3 characters')
# store in private attribute
        self._name=name
# only use get no set meaning immutable
    @property
    def name(self):
        return self._name
# find all orders for coffee abstaction used to hide the complexity of searching
    def orders(self):
        return[order for order in Order.all_orders if order.coffee==self]
# find the unique customers that have ordered this coffee
    def customers(self):
# then get all the orders for this coffee
        coffee_orders=self.orders() #abstraction using the order method
# extract the customer from order
        customer_list=[order.customer for order in coffee_orders]
# return unique customers (no duplicates)
        unique_customers=list(set(customer_list))
        return unique_customers
# count the total number of orders for coffee
    def num_orders(self):
        return len(self.orders())
# calculate the average price
    def average_price(self):
        coffee_orders=self.orders()
# if no orders exist
        if not coffee_orders:
            return 0
# sum the prices of all orders for this coffee
        total_price=sum(order.price for order in coffee_orders)
        average=total_price/len(coffee_orders)
# round to 2 decimal places
        return round(average,2)
        



