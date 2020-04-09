import operator


class Node:
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self, ctx):
        return self.statements.eval(ctx)


class Scope(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self, ctx):
        return self.statements.eval(ctx)


class Statements(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self, ctx):
        value = None
        for statement in self.statements:
            value = statement.eval(ctx)
        return value


class Statement(Node):
    def __init__(self, statement):
        self.statement = statement

    def eval(self, ctx):
        return self.statement.eval(ctx)


class Define(Node):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def eval(self, ctx):
        ctx.symbol_define(self.symbol, self.value.eval(ctx))
        return None


class Assign(Node):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def eval(self, ctx):
        ctx.symbol_assign(self.symbol, self.value.eval(ctx))
        return None


class Print(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, ctx):
        print(self.value.eval(ctx))
        return None


class ValueInt(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, ctx):
        return self.value


class ValueFloat(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, ctx):
        return self.value


class ValueString(Node):
    def __init__(self, value):
        self.value = value[1:-1]

    def eval(self, ctx):
        return self.value


class ValueSymbol(Node):
    def __init__(self, symbol):
        self.symbol = symbol

    def eval(self, ctx):
        return ctx.symbol_get(self.symbol)


class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, ctx):
        left = self.left.eval(ctx)
        right = self.right.eval(ctx)

        if not isinstance(left, type(right)):
            ltype = self.left.__class__.__name__
            rtype = self.right.__class__.__name__
            raise ValueError(f"Type mismatch between {ltype} and {rtype}")
        elif isinstance(left, ValueString) and self.op is not operator.add:
            raise ValueError("Invalid string operation")
        else:
            return self.op(left, right)


class Cast(Node):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def eval(self, ctx):
        type = self.type.gettokentype()
        assert type in ("INT", "FLOAT", "STRING")
        if type == "INT":
            return int(self.value.eval(ctx))
        elif type == "FLOAT":
            return float(self.value.eval(ctx))
        elif type == "STRING":
            return str(self.value.eval(ctx))
