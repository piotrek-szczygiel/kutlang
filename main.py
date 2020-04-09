from rply import LexingError, ParsingError

from lang.lexer import Lexer
from lang.parser import Parser
from lang.context import Context

lexer = Lexer()
parser = Parser(lexer.tokens)

ctx = Context()
while True:
    try:
        line = input("> ")

        tokens = lexer.lex(line)
        ast = parser.parse(tokens)

        result = ast.eval(ctx)
        if result is not None:
            print(result)

    except KeyboardInterrupt:
        break

    except ValueError as err:
        print(err)

    except LexingError as err:
        print(f"Lexing error: {err}")

    except ParsingError as err:
        print(f"Parsing error: {err}")
