import sys

from rply import LexingError, ParsingError

from lang.lexer import Lexer
from lang.parser import Parser
from lang.scope import Scope

lexer = Lexer()
parser = Parser(lexer.tokens)
scope = Scope()


def execute(scope, source):
    try:
        tokens = lexer.lex(source)
        ast = parser.parse(tokens)
        return ast.eval(scope)
    except ValueError as err:
        print(err)
    except LexingError as err:
        pos = err.getsourcepos()
        print(f"{pos.lineno}:{pos.colno} Lexing error")
    except ParsingError as err:
        pos = err.getsourcepos()
        print(f"{pos.lineno}:{pos.colno} Parsing error")


def repl():
    while True:
        try:
            source = input("> ")
            result = execute(scope, source)
            if result is not None:
                print(result)
        except KeyboardInterrupt:
            break


def file(path):
    with open(path, "r") as f:
        source = f.read()
        execute(scope, source)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    elif len(sys.argv) == 2:
        file(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} [file]")
