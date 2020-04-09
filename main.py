from rply import LexingError, ParsingError

from lang import ast
from lang.lexer import Lexer
from lang.parser import Parser

lexer = Lexer()
parser = Parser(lexer.tokens)

while True:
    s = input("> ")
    lexing_result = lexer.lex(s)
    try:
        parsing_result = parser.parse(lexing_result)
        parsing_result.eval()
    except ValueError as err:
        print(err)
    except LexingError as err:
        print(f"Lexing error: {err}")
    except ParsingError as err:
        print(f"Parsing error: {err}")
