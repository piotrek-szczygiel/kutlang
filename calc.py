import math
import sys
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    "NAME",
    "NUMBER",
    "POWER",
    "FUNCTION",
)


literals = ["=", "+", "-", "*", "/", "^", "(", ")", ";"]


def t_NUMBER(t):
    r"\d+\.\d+|\d+\.|\.\d+|\d+"
    t.value = float(t.value)
    return t


def t_POWER(t):
    r"\*\*"
    t.value = "^"
    return t


def t_FUNCTION(t):
    r"abs|asin|acos|atan|sin|cos|tan|exp|sqrt|log|ln"
    if t.value == "ln":  # ln is logarithm with base of e
        method = math.log
    elif t.value == "log":  # log is logarithm with base of 10
        method = lambda x: math.log(x, 10)
    elif t.value == "abs":  # fabs is floating-point absolute value
        method = math.fabs
    else:
        method = getattr(math, t.value)
    t.value = (t.value, method)
    return t


t_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer

lexer = lex.lex()

# Parsing rules

precedence = (
    ("left", "+", "-"),
    ("left", "*", "/"),
    ("right", "POWER"),
    ("right", "UMINUS"),
    ("right", "FUNCTION"),
)

# dictionary of names
names = {}


def p_program(p):
    """program : statement ';'
               | statement
               | statement ';' program"""


def p_statement_assign(p):
    """statement : NAME '=' expression"""
    names[p[1]] = p[3]


def p_statement_expr(p):
    """statement : expression"""
    trim = int(p[1])
    print(trim if trim == p[1] else p[1])


def p_expression_function(p):
    """expression : FUNCTION expression"""
    p[0] = p[1][1](p[2])


def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression POWER expression"""
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]
    elif p[2] == "^":
        p[0] = p[1] ** p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

while True:
    try:
        s = input("> ")
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
