class Symbols:
    def __init__(self):
        self.symbols = {}
        self.used = {}
        self.returnable = False
        self.breakable = False

    def add(self, name, value):
        self.symbols[name] = value
        self.used[name] = False

    def set(self, name, value):
        symbol = self.symbols[name]
        if not isinstance(symbol, type(value)):
            ltype = symbol.__class__.__name__
            rtype = value.__class__.__name__
            raise ValueError(
                f"Cannot assign {name} of type {rtype} to variable of type {ltype}"
            )
        self.symbols[name] = value

    def get(self, name):
        self.used[name] = True
        return self.symbols[name]

    def contains(self, name):
        return name in self.symbols


class Scope:
    def __init__(self):
        self.symbols_stack = [Symbols()]

    def add(self, name, value):
        if self.symbols_stack[0].contains(name):
            raise ValueError(f"Identifier '{name}' is already defined")
        else:
            self.symbols_stack[0].add(name, value)

    def set(self, name, value):
        found = False
        for symbols in self.symbols_stack:
            if symbols.contains(name):
                symbols.set(name, value)
                found = True
                break
        if not found:
            raise ValueError(f"Undefined identifier '{name}'")

    def get(self, name):
        for symbols in self.symbols_stack:
            if symbols.contains(name):
                return symbols.get(name)
        raise ValueError(f"Undefined identifier '{name}'")

    def push(self):
        self.symbols_stack.insert(0, Symbols())

    def pop(self):
        return self.symbols_stack.pop(0)
