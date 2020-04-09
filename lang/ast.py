import operator


class Node:
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self):
        self.statements.eval()


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self):
        for statement in self.statements:
            statement.eval()


class Statement(Node):
    def __init__(self, statement):
        self.statement = statement

    def eval(self):
        self.statement.eval()


class ValueInt(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class ValueFloat(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class ValueString(Node):
    def __init__(self, value):
        self.value = value[1:-1]

    def eval(self):
        return self.value


class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if not isinstance(left, type(right)):
            ltype = self.left.__class__.__name__
            rtype = self.right.__class__.__name__
            raise ValueError(f"Type mismatch between {ltype} and {rtype}")
        elif isinstance(left, ValueString) and self.op is not operator.add:
            raise ValueError("Invalid string operation")
        else:
            return self.op(left, right)


class Print(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())


class Cast(Node):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def eval(self):
        type = self.type.gettokentype()
        assert type in ("INT", "FLOAT", "STRING")
        if type == "INT":
            return int(self.value.eval())
        elif type == "FLOAT":
            return float(self.value.eval())
        elif type == "STRING":
            return str(self.value.eval())
