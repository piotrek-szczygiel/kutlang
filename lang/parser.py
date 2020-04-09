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
                ("left", ["OR"]),
                ("left", ["AND"]),
                ("right", ["NOT"]),
                ("left", ["EQ", "NE", "LE", "GE", "LT", "GT"]),
                ("left", ["ADD", "SUB"]),
                ("left", ["MUL", "DIV", "MOD"]),
                ("right", ["MINUS"]),
                ("right", ["POW"]),
                ("nonassoc", ["LPAREN", "RPAREN"]),
            ],
            cache_id="lang",
        )

        @pg.production("program : block")
        def program(p):
            return ast.Program(p[0])

        @pg.production("scope : LBRACE block RBRACE")
        def scope(p):
            return ast.BlockScoped(p[1])

        @pg.production("block : block stmt")
        def block(p):
            return ast.Block(p[0].block + [p[1]])

        @pg.production("block : stmt")
        def block_stmt(p):
            return ast.Block([p[0]])

        @pg.production("stmt : FN SYMBOL LPAREN def_args RPAREN scope")
        def stmt_fn(p):
            return ast.Fn(p[1].getstr(), p[3], p[5])

        @pg.production("def_args : def_args COMMA def_arg")
        def def_args(p):
            return p[0] + [p[2]]

        @pg.production("def_args : def_arg")
        def def_args_arg(p):
            return [p[0]]

        @pg.production("def_args :")
        def def_args_empty(p):
            return []

        @pg.production("def_arg : SYMBOL COLON type")
        def def_arg(p):
            return (p[0].getstr(), p[2])

        @pg.production("stmt : SYMBOL DEFINE expr")
        def stmt_define(p):
            return ast.Define(p[0].getstr(), p[2])

        @pg.production("stmt : SYMBOL ASSIGN expr")
        def stmt_assign(p):
            return ast.Assign(p[0].getstr(), p[2])

        @pg.production("stmt : PRINTLN LPAREN expr RPAREN")
        @pg.production("stmt : PRINT LPAREN expr RPAREN")
        def stmt_print(p):
            if p[0].gettokentype() == "PRINTLN":
                return ast.Print(p[2], True)
            elif p[0].gettokentype() == "PRINT":
                return ast.Print(p[2], False)

        @pg.production("stmt : expr")
        def stmt_expr(p):
            return ast.Statement(p[0])

        @pg.production("expr : SYMBOL LPAREN args RPAREN")
        def expr_call(p):
            return ast.Call(p[0].getstr(), p[2])

        @pg.production("args : args COMMA expr")
        def args(p):
            return p[0] + [p[2]]

        @pg.production("args : expr")
        def args_expr(p):
            return [p[0]]

        @pg.production("args :")
        def args_empty(p):
            return []

        @pg.production("expr : IF expr scope ELSE scope")
        def expr_if_else(p):
            return ast.IfElse(p[1], p[2], p[4])

        @pg.production("expr : IF expr scope")
        def expr_if(p):
            return ast.If(p[1], p[2])

        @pg.production("expr : WHILE expr scope")
        def expr_while(p):
            return ast.While(p[1], p[2])

        @pg.production("expr : FOR stmt SC expr SC stmt scope")
        def expr_for(p):
            return ast.For(p[1], p[3], p[5], p[6])

        @pg.production("expr : MINUS expr")
        def expr_minus(p):
            return ast.Minus(p[1])

        @pg.production("expr : NOT expr")
        def expr_not(p):
            return ast.Not(p[1])

        @pg.production("expr : SYMBOL")
        def expr_symbol(p):
            return ast.ValueSymbol(p[0].getstr())

        @pg.production("expr : CAST LPAREN type COMMA expr RPAREN")
        def expr_cast(p):
            return ast.Cast(p[2], p[4])

        @pg.production("type : INT")
        @pg.production("type : FLOAT")
        @pg.production("type : STR")
        @pg.production("type : BOOL")
        def expr_type(p):
            return ast.Type(p[0].gettokentype())

        @pg.production("expr : VALUE_INT")
        def expr_number_int(p):
            return ast.ValueInt(int(p[0].getstr()))

        @pg.production("expr : VALUE_FLOAT")
        def expr_number_float(p):
            return ast.ValueFloat(float(p[0].getstr()))

        @pg.production("expr : VALUE_STR")
        def expr_str(p):
            return ast.ValueString(p[0].getstr())

        @pg.production("expr : TRUE")
        def expr_true(p):
            return ast.ValueTrue()

        @pg.production("expr : FALSE")
        def expr_false(p):
            return ast.ValueFalse()

        @pg.production("expr : LPAREN expr RPAREN")
        def expr_parens(p):
            return p[1]

        @pg.production("expr : expr ADD expr")
        @pg.production("expr : expr SUB expr")
        @pg.production("expr : expr MUL expr")
        @pg.production("expr : expr DIV expr")
        @pg.production("expr : expr POW expr")
        @pg.production("expr : expr MOD expr")
        @pg.production("expr : expr EQ expr")
        @pg.production("expr : expr NE expr")
        @pg.production("expr : expr LE expr")
        @pg.production("expr : expr GE expr")
        @pg.production("expr : expr LT expr")
        @pg.production("expr : expr GT expr")
        @pg.production("expr : expr AND expr")
        @pg.production("expr : expr OR expr")
        def expr_binop(p):
            left = p[0]
            right = p[2]

            methods = {
                "ADD": operator.add,
                "SUB": operator.sub,
                "MUL": operator.mul,
                "DIV": operator.truediv,
                "POW": operator.pow,
                "MOD": operator.mod,
                "EQ": operator.eq,
                "NE": operator.ne,
                "LE": operator.le,
                "GE": operator.ge,
                "LT": operator.lt,
                "GT": operator.gt,
                "AND": operator.and_,
                "OR": operator.or_,
            }

            op = p[1].gettokentype()
            assert op in methods
            return ast.BinaryOp(methods[op], left, right)

        return pg.build()
