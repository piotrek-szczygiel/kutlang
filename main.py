import operator
from rply import LexerGenerator, ParserGenerator, ParsingError

lg = LexerGenerator()

lg.ignore(r"\s+")


tokens = []


def add_token(token, regexp):
    tokens.append(token)
    lg.add(token, regexp)


add_token("LPAREN", r"\(")
add_token("RPAREN", r"\)")

# add_token("LBRACE", r"\{")
# add_token("RBRACE", r"\}")
# add_token("DEFINE_ASSIGN", r":=")
# add_token("RETURNS_ARROW", r"->")
# add_token("COMMA", r",")
# add_token("COLON", r":")
# add_token("SEMICOLON", r";")
# add_token("EQUAL", r"==")
# add_token("ASSIGN", r"=")
# add_token("LOWER_EQUAL", r"<=")
# add_token("GREATER_EQUAL", r">=")
# add_token("LOWER", r"<")
# add_token("GREATER", r">")

add_token("PLUS", r"\+")
add_token("MINUS", r"-")
add_token("MUL", r"\*")
add_token("DIV", r"/")
add_token("POW", r"\^")

add_token("NUMBER_FLOAT", r"\d+\.\d+|\d+\.|\.\d+")
add_token("NUMBER_INT", r"\d+")
add_token("STRING", r"\"(.*?)\"")

# add_token("IF", r"if")
# add_token("ELSE", r"else")
# add_token("FN", r"fn")
# add_token("FOR", r"for")
# add_token("WHILE", r"while")
# add_token("RETURN", r"return")
# add_token("CAST", r"cast")
# add_token("PRINT", r"print")
# add_token("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*")

lexer = lg.build()


class ParsingSyntaxError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Syntax error: {self.message}"


class AstNode:
    pass


class NumberInt(AstNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class NumberFloat(AstNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class String(AstNode):
    def __init__(self, value):
        self.value = value[1:-1]

    def eval(self):
        return self.value


class BinaryOp(AstNode):
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
            raise ParsingSyntaxError(f"Type mismatch between {ltype} and {rtype}")
        elif isinstance(left, String) and self.op is not operator.add:
            raise ParsingSyntaxError("Invalid string operation")
        else:
            return self.op(left, right)


pg = ParserGenerator(
    tokens,
    precedence=[
        ("left", ["PLUS", "MINUS"]),
        ("left", ["MUL", "DIV"]),
        ("right", ["POW"]),
    ],
)


@pg.production("expression : NUMBER_INT")
def expression_number_int(p):
    return NumberInt(int(p[0].getstr()))


@pg.production("expression : NUMBER_FLOAT")
def expression_number_float(p):
    return NumberFloat(float(p[0].getstr()))


@pg.production("expression : STRING")
def expression_string(p):
    return String(p[0].getstr())


@pg.production("expression : LPAREN expression RPAREN")
def expression_parens(p):
    return p[1]


@pg.production("expression : expression PLUS expression")
@pg.production("expression : expression MINUS expression")
@pg.production("expression : expression MUL expression")
@pg.production("expression : expression DIV expression")
@pg.production("expression : expression POW expression")
def expression_binop(p):
    left = p[0]
    right = p[2]
    op = p[1].gettokentype()
    if op == "PLUS":
        return BinaryOp(operator.add, left, right)
    elif op == "MINUS":
        return BinaryOp(operator.sub, left, right)
    elif op == "MUL":
        return BinaryOp(operator.mul, left, right)
    elif op == "DIV":
        return BinaryOp(operator.truediv, left, right)
    elif op == "POW":
        return BinaryOp(operator.pow, left, right)
    else:
        raise AssertionError("Unknown binary operator")


@pg.error
def error_handler(token):
    raise ParsingSyntaxError(f"Unexpected token: {token.gettokentype()}")


parser = pg.build()

while True:
    s = input("> ")
    lexing_result = lexer.lex(s)
    parsing_result = parser.parse(lexing_result)
    try:
        eval_result = parsing_result.eval()
        print(eval_result)
    except ParsingSyntaxError as err:
        print(err)
