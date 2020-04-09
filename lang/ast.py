import operator


class Node:
    pass


class Program(Node):
    def __init__(self, block):
        self.block = block

    def eval(self, ctx):
        return self.block.eval(ctx)


class Scope(Node):
    def __init__(self, block):
        self.block = block

    def eval(self, ctx):
        return self.block.eval(ctx)


class Block(Node):
    def __init__(self, block):
        self.block = block

    def eval(self, ctx):
        value = None
        for stmt in self.block:
            value = stmt.eval(ctx)
        return value


class Statement(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def eval(self, ctx):
        return self.stmt.eval(ctx)


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


class ValueTrue(Node):
    def eval(self, ctx):
        return True


class ValueFalse(Node):
    def eval(self, ctx):
        return False


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


class If(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def eval(self, ctx):
        if self.cond.eval(ctx):
            return self.block.eval(ctx)


class IfElse(Node):
    def __init__(self, cond, true_block, false_block):
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

    def eval(self, ctx):
        if self.cond.eval(ctx):
            return self.true_block.eval(ctx)
        else:
            return self.false_block.eval(ctx)


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def eval(self, ctx):
        value = None
        while self.cond.eval(ctx):
            value = self.block.eval(ctx)
        return value


class For(Node):
    def __init__(self, begin, cond, step, block):
        self.begin = begin
        self.cond = cond
        self.step = step
        self.block = block

    def eval(self, ctx):
        self.begin.eval(ctx)
        value = None
        while self.cond.eval(ctx):
            value = self.block.eval(ctx)
            self.step.eval(ctx)
        return value


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
