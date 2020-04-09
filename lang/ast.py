import operator

from lang.scope import Scope


class Node:
    pass


class Program(Node):
    def __init__(self, block):
        self.block = block

    def eval(self, scope):
        return self.block.eval(scope)


class BlockScoped(Node):
    def __init__(self, block):
        self.block = block

    def eval(self, scope, args={}):
        scope.push()
        scope.set_breakable()
        for name, value in args.items():
            scope.add(name, value)
        value = self.block.eval(scope)
        scope.pop()
        return value


class Block(Node):
    def __init__(self, block):
        self.block = block

    def eval(self, scope):
        value = None
        for stmt in self.block:
            value = stmt.eval(scope)
        return value


class Statement(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def eval(self, scope):
        return self.stmt.eval(scope)


class Fn(Node):
    def __init__(self, symbol, args, block):
        self.symbol = symbol
        self.args = args
        self.block = block

    def eval(self, scope):
        scope.add(self.symbol, (self.args, self.block))


class Define(Node):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def eval(self, scope):
        scope.add(self.symbol, self.value.eval(scope))
        return None


class Assign(Node):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def eval(self, scope):
        scope.set(self.symbol, self.value.eval(scope))
        return None


class Print(Node):
    def __init__(self, value, newline):
        self.value = value
        self.newline = newline

    def eval(self, scope):
        if self.newline:
            print(self.value.eval(scope))
        else:
            print(self.value.eval(scope), end="")
        return None


class ValueInt(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        return self.value


class ValueFloat(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        return self.value


class ValueString(Node):
    def __init__(self, value):
        self.value = value[1:-1]

    def eval(self, scope):
        return self.value


class ValueTrue(Node):
    def eval(self, scope):
        return True


class ValueFalse(Node):
    def eval(self, scope):
        return False


class ValueSymbol(Node):
    def __init__(self, symbol):
        self.symbol = symbol

    def eval(self, scope):
        return scope.get(self.symbol)


class Type(Node):
    def __init__(self, type):
        types = {
            "INT": int,
            "FLOAT": float,
            "STR": str,
            "BOOL": bool,
        }

        self.type = types[type]

    def eval(self, scope):
        return self.type


class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, scope):
        left = self.left.eval(scope)
        right = self.right.eval(scope)

        if not isinstance(left, type(right)):
            ltype = self.left.__class__.__name__
            rtype = self.right.__class__.__name__
            raise ValueError(f"Type mismatch between {ltype} and {rtype}")
        elif isinstance(left, ValueString) and self.op is not operator.add:
            raise ValueError("Invalid string operation")
        else:
            return self.op(left, right)


class If(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def eval(self, scope):
        if self.cond.eval(scope):
            return self.block.eval(scope)


class IfElse(Node):
    def __init__(self, cond, true_block, false_block):
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

    def eval(self, scope):
        if self.cond.eval(scope):
            return self.true_block.eval(scope)
        else:
            return self.false_block.eval(scope)


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def eval(self, scope):
        value = None
        while self.cond.eval(scope):
            value = self.block.eval(scope)
        return value


class For(Node):
    def __init__(self, begin, cond, step, block):
        self.begin = begin
        self.cond = cond
        self.step = step
        self.block = block

    def eval(self, scope):
        self.begin.eval(scope)
        value = None
        while self.cond.eval(scope):
            value = self.block.eval(scope)
            self.step.eval(scope)
        return value


class Minus(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        value = self.value.eval(scope)
        if not isinstance(value, int) and not isinstance(value, float):
            type = value.__class__.__name__
            raise ValueError(f"Cannot negate {type}")
        return value * -1


class Not(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        value = self.value.eval(scope)
        if not isinstance(value, bool):
            type = value.__class__.__name__
            raise ValueError(f"Cannot negate {type}")
        return not value


class Cast(Node):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def eval(self, scope):
        cast = self.type.eval(scope)
        return cast(self.value.eval(scope))


class Call(Node):
    def __init__(self, symbol, args):
        self.symbol = symbol
        self.args = args

    def eval(self, scope):
        types, fn = scope.get(self.symbol)
        if len(self.args) != len(types):
            raise ValueError(f"Invalid number of arguments passed to '{self.symbol}'")

        args = {}
        for i in range(len(types)):
            value = self.args[i].eval(scope)
            name, type = types[i]
            type = type.eval(scope)
            if not isinstance(value, type):
                ltype = value.__class__.__name__
                rtype = type.__name__
                raise ValueError(f"Argument type mismatch between {ltype} and {rtype}")
            args[name] = value

        scope = Scope()
        return fn.eval(scope, args)
