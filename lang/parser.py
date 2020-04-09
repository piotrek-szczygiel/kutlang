import operator

from rply import ParserGenerator

from lang import ast


class Parser:
    def __init__(self, tokens):
        self.parser = Parser.create_parser(tokens)

    def parse(self, input):
        return self.parser.parse(input)

    @staticmethod
    def create_parser(tokens):
        pg = ParserGenerator(
            tokens,
            precedence=[
                ("left", ["ADD", "SUB"]),
                ("left", ["MUL", "DIV"]),
                ("right", ["POW"]),
            ],
            cache_id="lang",
        )

        @pg.production("program : statements")
        def program(p):
            return ast.Program(p[0])

        @pg.production("statements : statements SEMICOLON statement")
        def statements(p):
            return ast.Statements(p[0].statements + [p[2]])

        @pg.production("statements : statement")
        def statements_statement(p):
            return ast.Statements([p[0]])

        @pg.production("statement : SYMBOL DEFINE expression")
        def statement_define(p):
            return ast.Define(p[0].getstr(), p[2])

        @pg.production("statement : SYMBOL ASSIGN expression")
        def statement_assign(p):
            return ast.Assign(p[0].getstr(), p[2])

        @pg.production("statement : PRINT LPAREN expression RPAREN")
        def statement_print(p):
            return ast.Print(p[2])

        @pg.production("statement : expression")
        def statement_expression(p):
            return ast.Statement(p[0])

        @pg.production(
            "expression : IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE"
        )
        def expression_if_else(p):
            return ast.IfElse(p[1], p[3], p[7])

        @pg.production("expression : IF expression LBRACE statements RBRACE")
        def expression_if(p):
            return ast.If(p[1], p[3])

        @pg.production("expression : SYMBOL")
        def expression_symbol(p):
            return ast.ValueSymbol(p[0].getstr())

        @pg.production("expression : CAST LPAREN INT COMMA expression RPAREN")
        @pg.production("expression : CAST LPAREN FLOAT COMMA expression RPAREN")
        @pg.production("expression : CAST LPAREN STRING COMMA expression RPAREN")
        def expression_cast(p):
            return ast.Cast(p[2], p[4])

        @pg.production("expression : VALUE_INT")
        def expression_number_int(p):
            return ast.ValueInt(int(p[0].getstr()))

        @pg.production("expression : VALUE_FLOAT")
        def expression_number_float(p):
            return ast.ValueFloat(float(p[0].getstr()))

        @pg.production("expression : VALUE_STRING")
        def expression_string(p):
            return ast.ValueString(p[0].getstr())

        @pg.production("expression : TRUE")
        def expression_true(p):
            return ast.ValueTrue()

        @pg.production("expression : FALSE")
        def expression_false(p):
            return ast.ValueFalse()

        @pg.production("expression : LPAREN expression RPAREN")
        def expression_parens(p):
            return p[1]

        @pg.production("expression : expression ADD expression")
        @pg.production("expression : expression SUB expression")
        @pg.production("expression : expression MUL expression")
        @pg.production("expression : expression DIV expression")
        @pg.production("expression : expression POW expression")
        def expression_binop(p):
            left = p[0]
            right = p[2]

            methods = {
                "ADD": operator.add,
                "SUB": operator.sub,
                "MUL": operator.mul,
                "DIV": operator.truediv,
                "POW": operator.pow,
            }

            op = p[1].gettokentype()
            assert op in methods
            return ast.BinaryOp(methods[op], left, right)

        return pg.build()
