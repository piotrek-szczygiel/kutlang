import sys

from rply import LexingError, ParsingError

from lang.lexer import Lexer
from lang.parser import Parser
from lang.context import Context

lexer = Lexer()
parser = Parser(lexer.tokens)
ctx = Context()


def execute(ctx, source):
    try:
        tokens = lexer.lex(source)
        ast = parser.parse(tokens)
        return ast.eval(ctx)
    except ValueError as err:
        print(err)
    except LexingError as err:
        pos = err.getsourcepos()
        print(f"{pos.lineno}:{pos.colno} Lexing error")
    except ParsingError as err:
        pos = err.getsourcepos()
        print(f"{pos.lineno}:{pos.colno} Prasing error")


def repl():
    while True:
        try:
            source = input("> ")
            result = execute(ctx, source)
            if result is not None:
                print(result)
        except KeyboardInterrupt:
            break


def file(path):
    with open(path, "r") as f:
        source = f.read()
        execute(ctx, source)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    elif len(sys.argv) == 2:
        file(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} [file]")
