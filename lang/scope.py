from collections import deque

from lang.symbols import Symbols


class Scope:
    def __init__(self):
        self.symbols_stack = deque([Symbols()])

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
        if not found:
            raise ValueError(f"Undefined identifier '{name}'")

    def get(self, name):
        for symbols in self.symbols_stack:
            if symbols.contains(name):
                return symbols.get(name)
        raise ValueError(f"Undefined identifier '{name}'")

    def push(self):
        self.symbols_stack.appendleft(Symbols())

    def pop(self):
        self.symbols_stack.popleft()
