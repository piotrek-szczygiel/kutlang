import operator
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    "NAME",
    "NUMBER",
    "REL_OP",
)

literals = ["=", "+", "-", "*", "/", "^"]


def t_NUMBER(t):
    r"\d+\.\d+|\d+\.|\.\d+|\d+"
    t.value = float(t.value)
    if t.value % 1 == 0:
        t.value = int(t.value)
    return t


t_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_REL_OP = r"<=|>=|<|>|==|!="
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

names = {}


def p_relation(p):
    """relation : expression REL_OP expression"""
    if p[2] == "<=":
        p[0] = p[1] <= p[3]
    elif p[2] == ">=":
        p[0] = p[1] >= p[3]
    elif p[2] == "<":
        p[0] = p[1] < p[3]
    elif p[2] == ">":
        p[0] = p[1] > p[3]
    elif p[2] == "==":
        p[0] = p[1] == p[3]
    elif p[2] == "!=":
        p[0] = p[1] != p[3]


def p_statement_assign(p):
    """statement : NAME '=' expression"""
    names[p[1]] = p[3]


def p_statement_expr(p):
    """statement : expression"""
    print(p[1])


def p_expression_rpn(p):
    """expression : rpn"""
    p[0] = p[1]


def p_expression_name(p):
    """expression : NAME"""
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_rpn(p):
    """rpn : number rpn_repeat"""
    program = [p[1]] + p[2]
    stack = []
    for x in program:
        if x[0] == "number":
            stack.append(x[1])
        elif x[0] == "op":
            try:
                a = stack.pop()
                b = stack.pop()
                stack.append(x[2](a, b))
            except IndexError:
                print("Stack is empty!")
                return

    if stack:
        p[0] = stack.pop()
    else:
        print("Stack is empty!")

    if len(stack) > 0:
        print("Unused variables left on stack:", stack)


def p_rpn_repeat(p):
    """rpn_repeat : rpn_repeat number
                  | rpn_repeat op
                  | """

    if len(p) == 1:  # epsilon
        p[0] = []
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]


def p_number(p):
    """number : NUMBER"""
    p[0] = ("number", p[1])


def p_op(p):
    """op : '+'
          | '-'
          | '*'
          | '/'
          | '^'"""
    if p[1] == "+":
        method = operator.add
    elif p[1] == "-":
        method = operator.sub
    elif p[1] == "*":
        method = operator.mul
    elif p[1] == "/":
        method = operator.div
    elif p[1] == "^":
        method = operator.pow
    p[0] = ("op", p[1], method)


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

while True:
    try:
        s = input("> ")
    except (KeyboardInterrupt, EOFError):
        break
    if not s:
        continue
    yacc.parse(s)
