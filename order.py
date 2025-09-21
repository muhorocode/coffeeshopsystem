# order class is the joiner class that connects a specific customer to a coffee at a sepecific price
class Order:
    all_orders=[]
    # data bundling
    def __init__(self,customer,coffee,price): #method definition
# price validation used encapsulation to protect my data
        if not isinstance(price,(int,float)) or price <1.0 or price>10.0:
            raise Exception ('price must be a number between 1.0 and 10.0')
# instance attribute storage used encapsulation to make attributes private(hidden and can not be accessed directly from the outside) with an underscore
        self._customer=customer #data
        self._coffee=coffee #data
        self._price=price #data
# adding the new order instance to the class variable all_orders
        Order.all_orders.append(self)
# properties to access the private attributes
# the @property makes a method act like an attribute
#    get and return the customer object for this order
# only read access 
    @property
    def customer(self):
        return self._customer
#    get and return the coffee object for this order
    @property
    def coffee(self):
        return self._coffee
#    get and return the price paid for this order
    @property
    def price(self):
        return self._price  

