import operator
import sys
import ply.lex as lex
import ply.yacc as yacc


keywords = (
    "IF",
    "WHILE",
    "FOR",
    "DEF",
    "RUN",
)

tokens = keywords + ("NAME", "NUMBER", "OP", "REL",)

literals = [
    "=",
    "(",
    ")",
    ";",
    "{",
    "}",
]


def t_NUMBER(t):
    r"\d+\.\d+|\d+\.|\.\d+|\d+"
    t.value = float(t.value)
    if t.value % 1 == 0:
        t.value = int(t.value)
    return t


def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    if t.value.upper() in keywords:
        t.type = t.value.upper()

    return t


t_REL = r"<=|>=|<|>|==|!="
t_OP = r"\+|-|\*|/|\^"
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_block(p):
    """block : statement
             | '{' statement ';' more_statements '}'
       more_statements : statement
                       | statement ';' more_statements
                       | """
    statements = []
    for x in p[1:]:
        if x in ("{", ";", "}"):
            continue
        statements.append(x)
    p[0] = ("block", statements)


def p_statement_def(p):
    """statement : DEF NAME '=' block"""
    p[0] = ("def", p[2], p[4])


def p_statement_run(p):
    """statement : RUN NAME"""
    p[0] = ("run", p[2])


def p_statement_for(p):
    """statement : FOR '(' statement ';' relation ';' statement ')' block"""
    p[0] = ("for", p[3], p[5], p[7], p[9])


def p_statement_while(p):
    """statement : WHILE '(' relation ')' block"""
    p[0] = ("while", p[3], p[5])


def p_statement_if(p):
    """statement : IF '(' relation ')' block"""
    p[0] = ("if", p[3], p[5])


def p_statement_assign(p):
    """statement : NAME '=' expression"""
    p[0] = ("assign", p[1], p[3])


def p_statement_print(p):
    """statement : expression"""
    p[0] = ("print", p[1])


def p_relation(p):
    """relation : expression rel expression"""
    p[0] = ("relation", p[2], p[1], p[3])


def p_expression(p):
    """expression : name
                  | number
                  | name rpn
                  | number rpn"""
    e = [p[1]]
    if len(p) == 3:
        e += p[2]
    p[0] = ("expr", e)


def p_rpn(p):
    """rpn : rpn number
           | rpn name
           | rpn op
           | """
    if len(p) == 1:
        p[0] = []
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]


def p_number(p):
    """number : NUMBER"""
    p[0] = ("number", p[1])


def p_name(p):
    """name : NAME"""
    p[0] = ("name", p[1])


def p_rel(p):
    """rel : REL"""
    p[0] = p[1]


def p_op(p):
    """op : OP"""
    p[0] = ("op", p[1])


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


names = {}
funs = {}

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}
rels = {
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
    "==": operator.eq,
    "!=": operator.ne,
}


def execute(p):
    fun = p[0]
    args = p[1:]

    if fun == "block":
        for stmt in args[0]:
            execute(stmt)
    elif fun == "print":
        result = execute(args[0])
        if result:
            print(result)
    elif fun == "assign":
        name = args[0]
        result = execute(args[1])
        names[name] = result
    elif fun == "def":
        name = args[0]
        block = args[1]
        funs[name] = block
    elif fun == "run":
        name = args[0]
        try:
            block = funs[name]
        except LookupError:
            print(f"Undefined function: '{name}'")
            return
        return execute(block)
    elif fun == "relation":
        rel = rels[args[0]]
        a = execute(args[1])
        b = execute(args[2])
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return rel(a, b)
    elif fun == "if":
        cond = args[0]
        then = args[1]
        if execute(cond):
            execute(then)
    elif fun == "while":
        cond = args[0]
        then = args[1]
        while execute(cond):
            execute(then)
    elif fun == "for":
        start = args[0]
        cond = args[1]
        step = args[2]
        then = args[3]
        execute(start)
        while execute(cond):
            execute(then)
            execute(step)
    elif fun == "expr":
        stack = []
        for x in args[0]:
            if x[0] == "number":
                stack.append(x[1])
            elif x[0] == "name":
                try:
                    stack.append(names[x[1]])
                except LookupError:
                    print(f"Undefined name '{x[1]}'")
                    return
            elif x[0] == "op":
                stack.append(ops[x[1]](stack.pop(), stack.pop()))

        if len(stack) == 1:
            return stack.pop()
        else:
            print(f"Invalid stack state: {stack}")


parser = yacc.yacc()


def parse(string):
    result = yacc.parse(string)
    if result:
        return execute(result)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            data = open(sys.argv[1]).read()
            parse(data)
        except FileNotFoundError:
            print(f"Unable to open file '{sys.argv[1]}'")
    else:
        string = ""
        while True:
            prompt = ". " if string else "> "
            try:
                s = input(prompt)
            except (KeyboardInterrupt, EOFError):
                break

            if not s:
                if not string:
                    break
                else:
                    parse(string)
                    string = ""
            elif s[-1] == " ":
                string += s[:-1]
                continue
            else:
                parse(string + s)
                string = ""
