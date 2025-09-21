# import Order class from the order file to create orders
from order import Order

class Customer:
    def __init__(self,name): #method definition(constructor method that runs when creating a new customer)
        self.name=name #triggers the setter for validation
    @property
# using the @property makes the method below act like an attribute
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
# name validation used encapsulation to protect data
        if not isinstance(value,str) or len (value) <1 or len (value) >15:
            raise Exception ('Name must be a string between 1 and 15 characters')
            # store the validated name in a private attribute with an underscore
        self._name=value
# find all orders for this customer
    def orders(self):
        return [order for order in Order.all_orders if order.customer==self]
# find all coffees this customer has ordered
    def coffees(self):
# then get all orders then the coffee ordered
        customer_orders=self.orders()
        coffee_list=[order.coffee for order in customer_orders]
# remove duplicates
        unique_coffees=list(set(coffee_list))
        return unique_coffees
# create a new order for this customer
    def create_order(self,coffee,price):
        return Order(self,coffee,price)

