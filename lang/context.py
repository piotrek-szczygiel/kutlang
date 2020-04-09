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
        self.symbols[name] = value

    def symbol_get(self, name):
        if name not in self.symbols:
            raise ValueError(f"Undefined identifier '{name}'")
        return self.symbols[name]
