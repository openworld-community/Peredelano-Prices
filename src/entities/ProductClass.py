class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def toString(self):
        return (f"Title: {self.name} ;  Price: {self.price}")

    def fill(self, name, price):
        self.name = name
        self.price = price
