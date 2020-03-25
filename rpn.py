import ply.lex as lex
import ply.yacc as yacc

tokens = ("NUMBER",)

literals = ["+", "-", "*", "/", "^"]


def t_NUMBER(t):
    r"\d+\.\d+|\d+\.|\.\d+|\d+"
    t.value = float(t.value)
    if t.value % 1 == 0:
        t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_rpn(p):
    """rpn : number rpn_repeat"""
    p[0] = [p[1]] + p[2]
    print(p[0])


def p_rpn_repeat(p):
    """rpn_repeat : rpn_repeat number
                  | rpn_repeat op
                  | """

    if len(p) == 1:  # epsilon
        p[0] = []
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]


def p_op(p):
    """op : '+'
          | '-'
          | '*'
          | '/'
          | '^'"""
    p[0] = p[1]


def p_number(p):
    """number : NUMBER"""
    p[0] = p[1]


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
