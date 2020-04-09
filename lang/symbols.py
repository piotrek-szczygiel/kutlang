class Symbols:
    def __init__(self):
        self.symbols = {}
        self.returnable = False
        self.breakable = False

    def add(self, name, value):
        self.symbols[name] = value

    def set(self, name, value):
        symbol = self.symbols[name]
        if not isinstance(symbol, type(value)):
            ltype = symbol.__class__.__name__
            rtype = value.__class__.__name__
            raise ValueError(f"Cannot assign {rtype} to variable of type {ltype}")
        self.symbols[name] = value

    def get(self, name):
        return self.symbols[name]

    def contains(self, name):
        return name in self.symbols
