class Context:
    def __init__(self):
        self.symbols = {}

    def symbol_define(self, name, value):
        if name in self.symbols:
            raise ValueError(f"Identifier '{name}' is already defined")
        self.symbols[name] = value

    def symbol_assign(self, name, value):
        if name not in self.symbols:
            raise ValueError(f"Undefined identifier '{name}'")
        symbol = self.symbols[name]
        if not isinstance(symbol, type(value)):
            ltype = symbol.__class__.__name__
            rtype = value.__class__.__name__
            raise ValueError(f"Cannot assign {rtype} to variable of type {ltype}")
        self.symbols[name] = value

    def symbol_get(self, name):
        if name not in self.symbols:
            raise ValueError(f"Undefined identifier '{name}'")
        return self.symbols[name]
