import argparse
import sys

from graphviz import Digraph
from rply import LexingError, ParsingError

from lang.lexer import Lexer
from lang.parser import Parser
from lang.scope import Scope

lexer = Lexer()
parser = Parser(lexer.tokens)
scope = Scope()


def execute(scope, source, draw=False):
    try:
        tokens = lexer.lex(source)
        ast = parser.parse(tokens)
        value = ast.eval(scope)

        if draw:
            g = Digraph()
            ast.draw(g)
            g.render("ast", format="png", view=True, cleanup=True)

        return value
    except ValueError as err:
        print(err)
    except LexingError as err:
        pos = err.getsourcepos()
        print(f"{pos.lineno}:{pos.colno} Lexing error")
    except ParsingError as err:
        pos = err.getsourcepos()
        print(f"{pos.lineno}:{pos.colno} Parsing error")


def run_repl(draw=False):
    while True:
        try:
            source = input("> ")
            result = execute(scope, source, draw)
            if result is not None:
                print(result)
        except KeyboardInterrupt:
            break


def run_file(path, draw):
    with open(path, "r") as f:
        source = f.read()
        execute(scope, source, draw)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file", nargs="?", help="path to script")
    arg_parser.add_argument(
        "-a", "--ast", help="draw abstract syntax tree", action="store_true"
    )
    args = arg_parser.parse_args()

    if args.file:
        run_file(args.file, args.ast)
    else:
        run_repl(args.ast)
